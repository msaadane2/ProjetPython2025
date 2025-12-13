# TD3_corpus_io.py
# Fonctions de création, sauvegarde et chargement du corpus
import os
import pandas as pd  # pour utiliser DataFrame
def construire_dataframe(docs_reddit, docs_arxiv):
    # Construire un DataFrame pandas à partir des documents Reddit et arXiv
    lignes = []
    i = 0  # identifiant
    # on ajoute les documents reddit
    for doc in docs_reddit:
        # accepter dict ou string
        if isinstance(doc, dict):
            ligne = doc.copy()
        else:
            ligne = {"texte": str(doc)}
        # garantir qu'on a toujours une colonne "texte"
        if "texte" not in ligne:
            ligne["texte"] = ""
        ligne["id"] = i
        ligne["origine"] = "reddit"
        lignes.append(ligne)
        i += 1
    # on ajoute les documents arxiv
    for doc in docs_arxiv:
        #  accepter dict ou string
        if isinstance(doc, dict):
            ligne = doc.copy()
        else:
            ligne = {"texte": str(doc)}
        # garantir qu'on a toujours une colonne "texte"
        if "texte" not in ligne:
            ligne["texte"] = ""
        ligne["id"] = i
        ligne["origine"] = "arxiv"
        lignes.append(ligne)
        i += 1
    # on transforme la liste en DataFrame
    df = pd.DataFrame(lignes)
    return df

def sauvegarder_corpus(df, chemin):
    # on crée le dossier s’il n’existe pas
    dossier = os.path.dirname(chemin)
    if dossier != "" and not os.path.exists(dossier):
        os.makedirs(dossier)
    # Notre choix du séparateur ';' pour compatibilité avec Excel au lieu du /t exigé par l'énoncé
    df.to_csv(chemin, sep=";", index=False, encoding="utf-8-sig")

def charger_corpus(chemin):
    # Le même séparateur est utilisé au chargement pour garantir la cohérence
    return pd.read_csv(chemin, sep=";", encoding="utf-8-sig")
