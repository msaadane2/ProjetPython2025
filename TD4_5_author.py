# TD4_5_author.py
# TD4 : définition de la classe Author
class Author:
    # Classe représentant un auteur
    def __init__(self, name):
        # nom de l’auteur
        self.name = name
        # nombre de documents écrits par l’auteur
        self.ndoc = 0
        # dictionnaire des documents de l’auteur
        self.production = {}
    def add(self, doc_id, doc):
        # ajoute un document à la production de l’auteur
        self.production[doc_id] = doc
        # incrémente le nombre de documents
        self.ndoc += 1
    def taille_moyenne(self):
        # calcule la taille moyenne des textes de l’auteur
        # la taille est mesurée en nombre de caractères
        if self.ndoc == 0:
            return 0
        total = 0
        # on additionne la taille de chaque texte
        for doc in self.production.values():
            total += len(doc.texte)
        # on divise par le nombre de documents
        return total / self.ndoc
    def __str__(self):
        # affichage simple de l’auteur
        return "Author(" + self.name + ", ndoc=" + str(self.ndoc) + ")"
