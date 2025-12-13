# TD3_stats.py

def afficher_stats(docs):
    # affiche le nombre total de documents
    print("Nombre de documents =", len(docs))
    # on parcourt chaque document
    for i, doc in enumerate(docs):
        # nombre de mots séparés par espace
        nb_mots = len(doc.split(" "))
        # nombre de phrases séparées par point
        nb_phrases = len(doc.split("."))
        print("Doc", i, ":", nb_mots, "mots /", nb_phrases, "phrases")

def filtrer_docs_trop_petits(docs):
    # liste pour stocker les bons documents
    nouveaux_docs = []
    # on garde seulement les docs >= 20 caractères
    for doc in docs:
        if len(doc) >= 20:
            nouveaux_docs.append(doc)
    return nouveaux_docs

def construire_gros_texte(docs):
    # on colle tous les textes en une seule chaîne
    return " ".join(docs)
