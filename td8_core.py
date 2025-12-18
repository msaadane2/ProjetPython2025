import pandas as pd
import re
from TD4_5_corpus import Corpus
from TD4_5_document import Document
from TD7_moteur_recherche import SearchEngine
def build_engine_from_csv(csv_path="discours_US.csv"):
    # charger le fichier CSV (tabulation)
    df = pd.read_csv(csv_path, sep="\t", on_bad_lines="skip", engine="python")
    # créer le corpus
    corpus = Corpus("discours_US")
    # découper un texte en phrases
    def decouper_en_phrases(texte):
        t = str(texte)
        phrases = re.split(r"[.!?]+", t)
        return [p.strip() for p in phrases if p.strip() != ""]
    # remplir le corpus
    for _, row in df.iterrows():
        auteur = row.get("speaker", "unknown")
        texte = row.get("text", "")
        for p in decouper_en_phrases(texte):
            doc = Document(
                titre="phrase_discours",
                auteur=str(auteur),
                date=str(row.get("date", "")),
                url=str(row.get("link", "")),
                texte=p
            )
            corpus.add_document(doc)
    # créer le moteur
    moteur = SearchEngine(corpus)
    return moteur, df
