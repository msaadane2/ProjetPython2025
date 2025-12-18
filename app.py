import re
import pandas as pd
import streamlit as st
from td8_core import build_engine_from_csv
from TD4_5_corpus import Corpus
from TD7_moteur_recherche import SearchEngine
from td6_traitement_texte import corpus_stats, corpus_concorde

# config page
st.set_page_config(page_title="TD8 + TD9-10", layout="wide")

# thème mauve
st.markdown("""
<style>
/* fond */
.stApp { background-color: #F6F0FA; }
/* titres */
h1, h2, h3 { color: #7B2CBF; }
/* boutons */
.stButton > button {
    background-color: #7B2CBF;
    color: white;
    border-radius: 8px;
    border: none;
}
.stButton > button:hover { background-color: #5A189A; }
/* onglets */
button[data-baseweb="tab"][aria-selected="true"]{
    color:#7B2CBF;
    border-bottom: 3px solid #7B2CBF;
}
/* inputs */
input { background-color:#FFFFFF !important; border-radius:6px !important; }
/* tableau */
[data-testid="stDataFrame"] { border: 1px solid #E0D7F3; }
/* messages -> mauve */
div[data-testid="stAlert"]{
    background-color: #EEE4F8;
    color: #2D1E3E;
    border-left: 6px solid #7B2CBF;
}
div[data-testid="stAlert"] svg { color: #7B2CBF; }
/* bar chart mauve  */
svg rect { fill: #7B2CBF !important; }
</style>
""", unsafe_allow_html=True)

# cache TD8
@st.cache_resource
def get_engine_td8(csv_path):
    return build_engine_from_csv(csv_path)

# cache TD9-10
@st.cache_resource
def load_td9_corpus_and_engine(corpus_path="data/corpus_complet.csv"):
    corpus = Corpus.load(corpus_path, nom="corpus_complet")
    moteur = SearchEngine(corpus)
    def get_type_local(doc):
        if hasattr(doc, "get_type"):
            return doc.get_type()
        return "document"
    def get_year_local(doc):
        d = str(getattr(doc, "date", "")).strip()
        m = re.search(r"(\d{4})", d)
        return int(m.group(1)) if m else None
    types = sorted(list({get_type_local(d) for d in corpus.id2doc.values()}))
    auteurs = sorted(list({str(d.auteur) for d in corpus.id2doc.values()}))
    years = [get_year_local(d) for d in corpus.id2doc.values()]
    years = [y for y in years if y is not None]
    ymin, ymax = (min(years), max(years)) if years else (2000, 2025)
    return corpus, moteur, types, auteurs, ymin, ymax
# sous-corpus
class MiniCorpus:
    def __init__(self, id2doc):
        self.id2doc = id2doc
# type d'un document
def get_doc_type(doc):
    if hasattr(doc, "get_type"):
        return doc.get_type()
    return "document"
# année d'un document
def get_doc_year(doc):
    d = str(getattr(doc, "date", "")).strip()
    m = re.search(r"(\d{4})", d)
    return int(m.group(1)) if m else None
# ids après filtres
def ids_filtres(corpus, type_sel="Tous", auteur_sel="Tous", year_min=None, year_max=None):
    ids = []
    for doc_id, doc in corpus.id2doc.items():
        t = get_doc_type(doc)
        a = str(doc.auteur)
        y = get_doc_year(doc)

        if type_sel != "Tous" and t != type_sel:
            continue
        if auteur_sel != "Tous" and a != auteur_sel:
            continue
        if year_min is not None and y is not None and y < year_min:
            continue
        if year_max is not None and y is not None and y > year_max:
            continue

        ids.append(doc_id)
    return ids

# onglets principaux
tab_td8, tab_td9 = st.tabs(["TD8", "TD9–TD10"])


# TD8 
with tab_td8:
    st.title("TD 8 : Moteur de recherche")
    # chemin du csv
    csv_path = st.text_input("Chemin CSV (TD8)", value="discours_US.csv")
    # charger moteur
    try:
        moteur8, _ = get_engine_td8(csv_path)
    except Exception as e:
        st.error(f"Chargement TD8 impossible : {e}")
        st.stop()
    # requête
    q8 = st.text_input("Requête (TD8)", placeholder="ex : freedom america")
    # top k
    k8 = st.slider("Top K (TD8)", 1, 30, 5)
    # lancer recherche
    if st.button("Rechercher (TD8)"):
        if q8.strip() == "":
            st.warning("Écris une requête")
        else:
            res = moteur8.search(q8, k8)
            if hasattr(res, "columns") and "score" in res.columns:
                res = res[res["score"] > 0]
            st.dataframe(res, use_container_width=True)


#  TD9–TD10
with tab_td9:
    st.title("TD9–TD10 : Mini-projet")
    # chemin du corpus
    corpus_path = st.text_input("Chemin corpus (TD9–TD10)", value="data/corpus_complet.csv")
    # charger corpus + moteur
    try:
        corpus9, moteur9, types9, auteurs9, ymin9, ymax9 = load_td9_corpus_and_engine(corpus_path)
    except Exception as e:
        st.error(f"Chargement corpus impossible : {e}")
        st.stop()
    # filtres
    colf1, colf2 = st.columns(2)
    with colf1:
        type_sel = st.selectbox("Type", options=["Tous"] + types9, index=0)
    with colf2:
        auteur_sel = st.selectbox("Auteur", options=["Tous"] + auteurs9, index=0)

    year_min, year_max = st.slider("Années", min_value=ymin9, max_value=ymax9, value=(ymin9, ymax9))

    # onglets TD9-10
    subtab1, subtab2, subtab3, subtab4 = st.tabs(["Recherche", "Occurrences", "Stats", "Comparaison"])
    # Recherche 
    with subtab1:
        st.subheader("Recherche (TD7)")
        # requête
        q = st.text_input("Requête", placeholder="ex : photo camera", key="td9_q")
        # top k
        k = st.slider("Top K", 1, 30, 5, key="td9_k")
        # lancer recherche
        if st.button("Rechercher", key="td9_btn_search"):
            if q.strip() == "":
                st.warning("Écris une requête")
            else:
                res = moteur9.search(q, max(50, k))
                # filtrer les résultats
                if hasattr(res, "columns") and "doc_id" in res.columns:
                    def ok(doc_id):
                        doc = corpus9.id2doc[int(doc_id)]
                        if type_sel != "Tous" and get_doc_type(doc) != type_sel:
                            return False
                        if auteur_sel != "Tous" and str(doc.auteur) != auteur_sel:
                            return False
                        y = get_doc_year(doc)
                        if y is not None and (y < year_min or y > year_max):
                            return False
                        return True
                    res = res[res["doc_id"].apply(ok)]
                # enlever scores 0
                if hasattr(res, "columns") and "score" in res.columns:
                    res = res[res["score"] > 0]
                # top k final
                res = res.head(k)
                if len(res) == 0:
                    st.info("Aucun résultat")
                else:
                    st.dataframe(res, use_container_width=True)


    # Occurrences
    with subtab2:
        st.subheader("Occurrences (TD6)")
        # mot à chercher
        motif = st.text_input("Mot", placeholder="ex : photo", key="td9_motif")
        # contexte
        ctx = st.slider("Contexte", 5, 80, 20, key="td9_ctx")
        # lancer occurrences
        if st.button("Afficher les occurrences", key="td9_btn_occ"):
            if motif.strip() == "":
                st.warning("Écris un mot")
            else:
                ids = ids_filtres(corpus9, type_sel, auteur_sel, year_min, year_max)
                sub = MiniCorpus({i: corpus9.id2doc[i] for i in ids})
                dfc = corpus_concorde(sub, motif.strip(), contexte=ctx)

                if len(dfc) == 0:
                    st.info("Aucune occurrence")
                else:
                    st.dataframe(dfc.head(30), use_container_width=True)


    # Stats
    with subtab3:
        st.subheader("Stats (TD6)")
        # top n
        topn = st.slider("Top N", 5, 50, 10, key="td9_topn")
        # lancer stats
        if st.button("Afficher les stats", key="td9_btn_stats"):
            ids = ids_filtres(corpus9, type_sel, auteur_sel, year_min, year_max)
            sub = MiniCorpus({i: corpus9.id2doc[i] for i in ids})
            freq = corpus_stats(sub, n=topn, avec_doc_freq=True)
            # top n
            freq_top = freq.head(topn)
            # tableau
            st.dataframe(freq_top, use_container_width=True)
            # chercher colonnes pour graphe
            col_txt = None
            for c in freq_top.columns:
                if freq_top[c].dtype == "object":
                    col_txt = c
                    break
            col_num = None
            for c in freq_top.columns:
                if pd.api.types.is_numeric_dtype(freq_top[c]):
                    col_num = c
                    break
            # graphe
            if col_txt is not None and col_num is not None:
                plot_df = freq_top[[col_txt, col_num]].set_index(col_txt)
                st.bar_chart(plot_df)
            else:
                st.info("Graphe non disponible")

    # Comparaison
    with subtab4:
        st.subheader("Comparaison Reddit vs ArXiv")
        # lancer comparaison
        if st.button("Comparer reddit vs arxiv", key="td9_btn_comp"):
            ids_reddit = ids_filtres(corpus9, "reddit", "Tous", year_min, year_max)
            ids_arxiv = ids_filtres(corpus9, "arxiv", "Tous", year_min, year_max)
            sub_r = MiniCorpus({i: corpus9.id2doc[i] for i in ids_reddit})
            sub_a = MiniCorpus({i: corpus9.id2doc[i] for i in ids_arxiv})
            st.write(f"Docs reddit : {len(ids_reddit)}  |  Docs arxiv : {len(ids_arxiv)}")
            st.write("Top mots reddit :")
            fr = corpus_stats(sub_r, n=10, avec_doc_freq=True)
            st.dataframe(fr.head(10), use_container_width=True)
            st.write("Top mots arxiv :")
            fa = corpus_stats(sub_a, n=10, avec_doc_freq=True)
            st.dataframe(fa.head(10), use_container_width=True)
