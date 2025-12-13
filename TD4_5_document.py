# TD4_5_document.py
# TD4 & TD5 : définition des documents et héritage
class Document:
    # Classe représentant un document générique
    def __init__(self, titre, auteur, date, url, texte):
        # informations communes à tous les documents
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
    def afficher(self):
        # affiche les informations principales du document
        print("Titre :", self.titre)
        print("Auteur :", self.auteur)
        print("Date :", self.date)
        print("URL :", self.url)
        # on affiche seulement les 200 premiers caractères du texte
        print("Texte :", self.texte[:200], "..." if len(self.texte) > 200 else "")
    def __str__(self):
        # affichage simple du document
        return self.titre
    def get_type(self):
        # type du document 
        return "document"
class RedditDocument(Document):
    # Classe représentant un document provenant de Reddit
    def __init__(self, titre, auteur, date, url, texte, nb_comments=0):
        # appel du constructeur de la classe Document
        super().__init__(titre, auteur, date, url, texte)
        # nombre de commentaires du post Reddit
        self.nb_comments = nb_comments
    # accesseur pour le nombre de commentaires
    def get_nb_comments(self):
        return self.nb_comments
    # mutateur pour le nombre de commentaires
    def set_nb_comments(self, n):
        self.nb_comments = n
    def get_type(self):
        # type spécifique du document
        return "reddit"
    def __str__(self):
        # affichage spécifique pour Reddit
        return "[Reddit] " + self.titre

class ArxivDocument(Document):
    # Classe représentant un document provenant d’arXiv
    def __init__(self, titre, auteur, date, url, texte, co_authors=None):
        # appel du constructeur de la classe Document
        super().__init__(titre, auteur, date, url, texte)
        # liste des co auteurs de l’article
        if co_authors is None:
            co_authors = []
        self.co_authors = co_authors
    # accesseur pour la liste des co-auteurs
    def get_co_authors(self):
        return self.co_authors
    # mutateur pour la liste des co-auteurs
    def set_co_authors(self, lst):
        self.co_authors = lst
    def get_type(self):
        # type spécifique du document
        return "arxiv"
    def __str__(self):
        # affichage spécifique pour arXiv
        return "[Arxiv] " + self.titre
