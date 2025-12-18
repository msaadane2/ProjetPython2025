# td6_traitement_texte.py
# TD6 : analyse de texte (regex + statistiques)
import re  # pour utiliser les expressions régulières
import pandas as pd  # pour créer des tableaux (DataFrame)
def nettoyer_texte(texte):
    # si le texte est vide
    if texte is None:
        return ""
    # transformer en texte
    t = str(texte)
    # mettre tout en minuscules
    t = t.lower()
    # remplacer retour ligne par espace
    t = t.replace("\n", " ")
    # remplacer tabulation par espace
    t = t.replace("\t", " ")
    # supprimer les chiffres
    t = re.sub(r"\d+", " ", t)
    # supprimer la ponctuation
    t = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ\s]", " ", t)
    # supprimer les espaces en trop
    t = re.sub(r"\s+", " ", t)
    # enlever espace début et fin
    return t.strip()

def tokenize(texte):
    # nettoyer le texte
    t = nettoyer_texte(texte)
    # si texte vide
    if t == "":
        return []
    # découper en mots
    return t.split(" ")

def construire_vocabulaire(docs):
    # set pour stocker mots uniques
    vocab = set()
    # parcourir les documents
    for txt in docs:
        # parcourir les mots du document
        for mot in tokenize(txt):
            # ajouter le mot s’il n’est pas vide
            if mot != "":
                vocab.add(mot)
    # retourner le vocabulaire trié
    return sorted(vocab)

def construire_freq(docs, vocab, avec_doc_freq=True):
    # dictionnaire fréquence totale
    tf = {mot: 0 for mot in vocab}
    # dictionnaire nombre de documents
    dfreq = {mot: 0 for mot in vocab}
    # parcourir les documents
    for txt in docs:
        # tokens du document
        tokens = tokenize(txt)
        # compter chaque mot
        for mot in tokens:
            if mot in tf:
                tf[mot] += 1
        # compter une seule fois par document
        if avec_doc_freq:
            for mot in set(tokens):
                if mot in dfreq:
                    dfreq[mot] += 1
    # liste pour le DataFrame
    lignes = []
    # construire chaque ligne
    for mot in vocab:
        ligne = {
            "mot": mot,
            "term_frequency": tf[mot]
        }
        # ajouter document_frequency 
        if avec_doc_freq:
            ligne["document_frequency"] = dfreq[mot]
        lignes.append(ligne)
    # créer le tableau
    freq = pd.DataFrame(lignes)
    # trier par fréquence décroissante
    freq = freq.sort_values(
        "term_frequency",
        ascending=False
    ).reset_index(drop=True)
    # retourner le tableau
    return freq

def extraire_gauche_droite(texte, motif, contexte=30):
    # liste des résultats
    resultats = []
    # chercher toutes les occurrences du motif
    for m in re.finditer(motif, texte, re.IGNORECASE):
        # début du motif
        debut = m.start()
        # fin du motif
        fin = m.end()
        # texte à gauche
        gauche = texte[max(0, debut - contexte):debut]
        # motif trouvé
        mot = texte[debut:fin]
        # texte à droite
        droite = texte[fin:min(len(texte), fin + contexte)]
        # ajouter le résultat
        resultats.append((gauche, mot, droite))
    # retourner les résultats
    return resultats

def corpus_search(corpus, motif, contexte=60):
    # liste des passages trouvés
    passages = []
    # parcourir les documents du corpus
    for doc_id, doc in corpus.id2doc.items():
        # récupérer le texte du document
        texte = str(doc.texte)
        # chercher le motif dans le document
        for g, m, d in extraire_gauche_droite(texte, motif, contexte):
            # ajouter le passage complet
            passages.append(g + m + d)
    # retourner les passages
    return passages

def corpus_concorde(corpus, motif, contexte=30):
    # liste pour le concordancier
    lignes = []
    # parcourir les documents
    for doc_id, doc in corpus.id2doc.items():
        # texte du document
        texte = str(doc.texte)
        # chercher les occurrences
        for g, m, d in extraire_gauche_droite(texte, motif, contexte):
            # ajouter une ligne
            lignes.append({
                "doc_id": doc_id,
                "contexte_gauche": g,
                "motif_trouve": m,
                "contexte_droit": d
            })
    # retourner le tableau
    return pd.DataFrame(lignes)

def corpus_stats(corpus, n=10, avec_doc_freq=True):
    # récupérer tous les textes
    docs = [str(doc.texte) for doc in corpus.id2doc.values()]
    # construire le vocabulaire
    vocab = construire_vocabulaire(docs)
    # construire la table de fréquence
    freq = construire_freq(docs, vocab, avec_doc_freq)
    # afficher infos demandées
    print("Nombre de mots différents =", len(vocab))
    print("Top", n, "mots les plus fréquents :")
    print(freq.head(n))
    # retourner le tableau
    return freq
