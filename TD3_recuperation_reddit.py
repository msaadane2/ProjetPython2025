# TD3_recuperation_reddit.py
#récupération de textes depuis reddit avec l'api praw
import praw # bibliothèque pour interroger l’API Reddit
import re # bibliothèque pour nettoyer le texte
# identifiants reddit (créés sur reddit apps)
REDDIT_CLIENT_ID = "aCRPicUkBSZXRk4POOBS6g"
REDDIT_CLIENT_SECRET = "WRwhWLpHk-CzfPsNS05kZ-aCgm_B7Q"

def nettoyer_sauts_de_ligne(texte):
    # enlève les retours à la ligne et espaces en trop
    if texte is None: #Si le texte est vide ou None, on renvoie une chaîne vide
        return ""
# Remplace les retours à la ligne par des espaces
    texte = texte.replace("\n", " ")
# Remplace les espaces multiples par un seul espace
    texte = re.sub(r"\s+", " ", texte)
# Supprime les espaces au début et à la fin
    return texte.strip()

def recuperer_textes_reddit(mot_cle, limit=10):
    # connexion à reddit avec praw: récupèrer des documents textuels depuis Reddit à partir d’un mot-clé
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="td3_photography_project"
    )
    docs = [] # liste pour stocker les textes récupérés
    # recherche des posts contenant le mot clé
    for submission in reddit.subreddit("all").search(mot_cle, limit=limit):
        # Récupération et nettoyage du titre du post
        titre = nettoyer_sauts_de_ligne(submission.title)
        # Récupération et nettoyage du contenu du post
        corps = nettoyer_sauts_de_ligne(submission.selftext)
        # on combine le titre et le texte du post
        texte = (titre + " " + corps).strip()
        # on garde seulement les textes non vides
        if texte != "":
            docs.append(texte)
    return docs  # on renvoie la liste des textes
from datetime import datetime
def recuperer_docs_reddit_complets(mot_cle, limit=10):
    # Version complète : récupère titre, auteur, date, url, texte, nb_comments POUR TD 4 & 5 
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="td3_photography_project"
    )
    docs = []
    # recherche des posts contenant le mot clé
    for submission in reddit.subreddit("all").search(mot_cle, limit=limit):
        titre = nettoyer_sauts_de_ligne(submission.title)
        corps = nettoyer_sauts_de_ligne(submission.selftext)
        # contenu textuel : corps sinon titre
        texte = (corps if corps != "" else titre).strip()
        if texte == "":
            continue
        auteur = str(submission.author) if submission.author else "unknown"
        date = datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d")
        url = "https://www.reddit.com" + submission.permalink
        nb_comments = int(submission.num_comments or 0)
        docs.append({
            "titre": titre,
            "auteur": auteur,
            "date": date,
            "url": url,
            "texte": texte,
            "nb_comments": nb_comments
        })
    return docs
