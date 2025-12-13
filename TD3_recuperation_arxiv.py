# TD3_recuperation_arxiv.py
# récupération de textes depuis arXiv avec l'api officielle
import urllib.request # pour envoyer des requêtes HTTP
import urllib.parse  # pour encoder le mot-clé dans l’URL
import xmltodict # pour parser le XML retourné par arXiv
import re # pour nettoyer le texte
def nettoyer_sauts_de_ligne(texte):
    # enlève les retours à la ligne et espaces en trop
    if texte is None:
        return ""
    texte = texte.replace("\n", " ")
    texte = re.sub(r"\s+", " ", texte)
    return texte.strip()

def recuperer_textes_arxiv(mot_cle, limit=10):
    # construit l'url de recherche arxiv
    # URL de base de l’API arXiv
    base_url = "http://export.arxiv.org/api/query?"
    # Construction de la requête avec le mot-clé et le nombre de résultats
    query = f"search_query=all:{urllib.parse.quote(mot_cle)}&start=0&max_results={limit}"
    url = base_url + query
    # envoie la requête à arxiv
    with urllib.request.urlopen(url) as response:
        data = response.read()
    # transforme le xml en dictionnaire python
    parsed = xmltodict.parse(data)
    feed = parsed.get("feed", {})
    entries = feed.get("entry", [])
    # cas où arxiv renvoie un seul résultat
    if isinstance(entries, dict):
        entries = [entries]
    docs = []  # liste des textes
    for entry in entries:
        resume = nettoyer_sauts_de_ligne(entry.get("summary", ""))
        if resume != "":
            docs.append(resume)
    return docs  # renvoie la liste des résumés

def recuperer_docs_arxiv_complets(mot_cle, max_results=10):
    # récupèrer titre, auteur, co_authors, date, url, texte POUR LE TD 4 ET 5
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query=all:{urllib.parse.quote(mot_cle)}&start=0&max_results={max_results}"
    url = base_url + query
    with urllib.request.urlopen(url) as response:
        data = response.read()
    parsed = xmltodict.parse(data)
    feed = parsed.get("feed", {})
    entries = feed.get("entry", [])
    # cas où arxiv renvoie un seul résultat
    if isinstance(entries, dict):
        entries = [entries]
    docs = []
    for entry in entries:
        titre = nettoyer_sauts_de_ligne(entry.get("title", ""))
        texte = nettoyer_sauts_de_ligne(entry.get("summary", ""))
        date = str(entry.get("published", ""))[:10]
        url_doc = str(entry.get("id", ""))
        # gestion des auteurs
        authors_field = entry.get("author", [])
        if isinstance(authors_field, dict):
            authors_field = [authors_field]
        authors = []
        for a in authors_field:
            name = a.get("name", "")
            # xmltodict peut renvoyer un dict au lieu d'une string
            if isinstance(name, dict):
                name = name.get("#text", "") or name.get("text", "") or ""
            # nettoyage
            name = str(name).strip()
            if name != "":
                authors.append(name)
        auteur = authors[0] if authors else "unknown"
        co_authors = authors[1:] if len(authors) > 1 else []
        # on garde seulement si on a du texte
        if texte != "":
            docs.append({
                "titre": titre,
                "auteur": auteur,
                "date": date,
                "url": url_doc,
                "texte": texte,
                "co_authors": co_authors
            })
    return docs
