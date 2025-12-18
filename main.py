# TD3 : Acquisition de données
import os
import pandas as pd
from TD3_recuperation_reddit import recuperer_textes_reddit, recuperer_docs_reddit_complets
from TD3_recuperation_arxiv import recuperer_textes_arxiv, recuperer_docs_arxiv_complets
from TD3_corpus_io import construire_dataframe, sauvegarder_corpus, charger_corpus
from TD3_stats import afficher_stats, filtrer_docs_trop_petits, construire_gros_texte
#TD4 / TD5 : Structuration du code avec des classes
from TD4_5_document import Document, RedditDocument, ArxivDocument
from TD4_5_corpus import Corpus
#TD 7 : moteur de recherche
from TD7_moteur_recherche import SearchEngine
# TD3 : Partie 1 : Chargement des données depuis Reddit et ArXiv
theme = "photography"
# TD3 , 4 & 5 : Sauvegarde des données
chemin_td3 = "data/corpus.csv"
chemin_td45 = "data/corpus_complet.csv"
# 2.3 Charger le DataFrame depuis le disque sans interroger les APIs
if os.path.exists(chemin_td3):
    df = charger_corpus(chemin_td3)
else:
    # 1.1 Reddit : récupérer le contenu textuel des documents liés à la thématique
    docs_reddit = recuperer_textes_reddit(theme, limit=5)
    # 1.2 ArXiv : récupérer le contenu textuel des documents liés à la thématique
    docs_arxiv = recuperer_textes_arxiv(theme, limit=5)
    # 2.1 Créer un DataFrame pandas avec id, texte et origine
    df = construire_dataframe(docs_reddit, docs_arxiv)
    # 2.2 Sauvegarder le DataFrame sur le disque au format CSV
    sauvegarder_corpus(df, chemin_td3)
# TD3 : Partie 3 : Premières manipulations des données
# 3.1 Afficher la taille du corpus
# 3.2 Afficher le nombre de mots et de phrases pour chaque document
docs = list(df["texte"])
afficher_stats(docs)
# 3.3 Supprimer les documents de moins de 20 caractères
docs = filtrer_docs_trop_petits(docs)
# 3.4 Créer une chaîne unique contenant tous les documents (join)
gros_texte = construire_gros_texte(docs)

# TD4 / TD5 : Structuration du code avec des classes
# (Ici on récupère les métadonnées complètes, indépendamment du TD3)
docs_reddit_complets = recuperer_docs_reddit_complets(theme, limit=5)
docs_arxiv_complets = recuperer_docs_arxiv_complets(theme, max_results=5)
df_complet = construire_dataframe(docs_reddit_complets, docs_arxiv_complets)
# mettre nb_comments à 0 si absent / NaN 
if "nb_comments" not in df_complet.columns:
    df_complet["nb_comments"] = 0
df_complet["nb_comments"] = df_complet["nb_comments"].fillna(0).astype(int)
# assurer co_authors propre pour Excel
if "co_authors" not in df_complet.columns:
    df_complet["co_authors"] = ""
df_complet.loc[df_complet["origine"] == "reddit", "co_authors"] = ""
corpus = Corpus("photography_corpus")
j = 0
for _, ligne in df_complet.iterrows():
    texte = str(ligne.get("texte", ""))
    origine = str(ligne.get("origine", ""))
    # même règle que TD3 : ignorer les docs trop petits
    if len(texte) < 20:
        continue
    if origine == "reddit": #reddit
        titre = str(ligne.get("titre", "Reddit " + str(j)))
        auteur = str(ligne.get("auteur", "unknown"))
        date = str(ligne.get("date", ""))
        url = str(ligne.get("url", ""))
        nb = ligne.get("nb_comments", 0)
        try:
            nb = 0 if pd.isna(nb) else int(nb)
        except Exception:
            nb = 0
        doc = RedditDocument(
            titre=titre,
            auteur=auteur,
            date=date,
            url=url,
            texte=texte,
            nb_comments=nb
        )
        # exemple d’utilisation du mutateur
        doc.set_nb_comments(nb)
    else: # arxiv
        titre = str(ligne.get("titre", "Arxiv " + str(j)))
        auteur = str(ligne.get("auteur", "unknown"))
        date = str(ligne.get("date", ""))
        url = str(ligne.get("url", ""))
        co = ligne.get("co_authors", [])
        # si c'est une string "a,b,c" :  liste
        if isinstance(co, str):
            co = [x.strip() for x in co.split(",") if x.strip() != ""]
        elif co is None or (isinstance(co, float) and pd.isna(co)):
            co = []
        doc = ArxivDocument(
            titre=titre,
            auteur=auteur,
            date=date,
            url=url,
            texte=texte,
            co_authors=co
        )
        # exemple d’utilisation du mutateur
        doc.set_co_authors(co)
    corpus.add_document(doc)
    j += 1
# sauvegarde du corpus complet
corpus.save(chemin_td45)
# TD4 &TD5 : test de rechargement (load) + affichage
corpus2 = Corpus.load(chemin_td45, nom="photography_corpus_reload")
corpus2.show(n=5, tri="titre")
# stats : prend un auteur qui existe vraiment
if len(corpus2.authors) > 0:
    premier_auteur = list(corpus2.authors.keys())[0]
    corpus2.stats_auteur(premier_auteur)
    
# affichage de la partie TD6 search
print("\nTD6 search")
res = corpus.search(r"photo")
print(res[:2]) # afficher seulement 2 résultats
# affichage du concordancier
print("\nTD6 concorde")
df_conc = corpus.concorde(r"photo", contexte=20)
print(df_conc.head())
# affichage des statistiques
print("\nTD6 stats")
corpus.stats(n=10, avec_doc_freq=True)

# Affichage TD7 : moteur de recherche
print("\nTD7 moteur de recherche")  # titre affiché
moteur = SearchEngine(corpus2)  # créer le moteur à partir du corpus
requete = input("Requête : ")  # l'utilisateur saisit les mots-clés
resultats = moteur.search(requete, nb_docs=5, use_tfidf=True)  # lancer la recherche
print(resultats)  # afficher les documents les plus pertinents

#Affichage TD8/9/10: interface utilisateur 
import subprocess
import sys
if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

