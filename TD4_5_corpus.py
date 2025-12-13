# TD4_5_corpus.py
# TD4 & TD5 : classe Corpus + sauvegarde/chargement + patrons (Factory, Singleton)
import os  # pour gérer les chemins et créer des dossiers
import pandas as pd  # pour utiliser DataFrame et CSV
from TD4_5_author import Author
from TD4_5_document import Document, RedditDocument, ArxivDocument
# TD5 : Factory = classe qui crée automatiquement le bon type de document
class DocumentFactory:
    @staticmethod
    def create(doc_type, **kwargs):
        # doc_type indique si c'est un document reddit, arxiv ou générique
        # si le type est reddit, on crée un RedditDocument
        if doc_type == "reddit":
            # sécuriser nb_comments si vide ou NaN
            nb = kwargs.get("nb_comments", 0)
            try:
                nb = 0 if pd.isna(nb) else int(nb)
            except Exception:
                nb = 0

            return RedditDocument(
                titre=kwargs.get("titre", ""),
                auteur=kwargs.get("auteur", ""),
                date=kwargs.get("date", ""),
                url=kwargs.get("url", ""),
                texte=kwargs.get("texte", ""),
                nb_comments=nb
            )
        # si le type est arxiv, on crée un ArxivDocument
        if doc_type == "arxiv":
            # les co auteurs peuvent être stockés en "a,b,c" dans le CSV
            co = kwargs.get("co_authors", [])
            if isinstance(co, str):
                co = [x.strip() for x in co.split(",") if x.strip() != ""]
            return ArxivDocument(
                titre=kwargs.get("titre", ""),
                auteur=kwargs.get("auteur", ""),
                date=kwargs.get("date", ""),
                url=kwargs.get("url", ""),
                texte=kwargs.get("texte", ""),
                co_authors=co
            )
        # sinon on crée un Document simple
        return Document(
            titre=kwargs.get("titre", ""),
            auteur=kwargs.get("auteur", ""),
            date=kwargs.get("date", ""),
            url=kwargs.get("url", ""),
            texte=kwargs.get("texte", "")
        )

class Corpus:
    # Singleton = on veut un seul corpus en mémoire
    _instance = None
    _already_init = False

    def __new__(cls, nom="corpus"):
        # si le corpus n'existe pas encore, on le crée
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        # sinon on renvoie toujours le même objet
        return cls._instance

    def __init__(self, nom="corpus"):
        # si déjà initialisé, on évite de remettre tout à zéro
        if Corpus._already_init:
            return
        Corpus._already_init = True
        # nom du corpus
        self.nom = nom
        # dictionnaire des auteurs : nom : Author
        self.authors = {}
        # dictionnaire des documents : id : Document
        self.id2doc = {}
        # nombre total de documents
        self.ndoc = 0
        # nombre total d'auteurs
        self.naut = 0

    def add_document(self, doc):
        # ajoute le document dans id2doc avec un id unique
        doc_id = self.ndoc
        self.id2doc[doc_id] = doc
        self.ndoc += 1
        # récupère le nom de l'auteur du document
        nom_auteur = str(doc.auteur)
        # si l'auteur n'existe pas encore, on le crée
        if nom_auteur not in self.authors:
            self.authors[nom_auteur] = Author(nom_auteur)
            self.naut += 1
        # on ajoute le document dans la production de l'auteur (dictionnaire)
        self.authors[nom_auteur].add(doc_id, doc)

    def __repr__(self):
        # affichage simple du corpus
        return "Corpus(" + self.nom + ", ndoc=" + str(self.ndoc) + ", naut=" + str(self.naut) + ")"

    def show(self, n=5, tri="titre"):
        # affiche les n premiers documents, triés par titre ou par date
        docs = list(self.id2doc.values())
        if tri == "date":
            docs.sort(key=lambda d: str(d.date))
        else:
            docs.sort(key=lambda d: str(d.titre))
        for i, doc in enumerate(docs[:n]):
            print(i, "-", str(doc))

    def stats_auteur(self, nom_auteur):
        # affiche des stats simples sur un auteur
        if nom_auteur not in self.authors:
            print("Auteur introuvable :", nom_auteur)
            return
        a = self.authors[nom_auteur]
        print("Auteur :", a.name)
        print("Nombre de documents :", a.ndoc)
        print("Taille moyenne (caractères) :", a.taille_moyenne())

    def save(self, chemin_csv):
        # sauvegarde le corpus dans un fichier CSV
        # si le dossier n'existe pas, on le crée
        dossier = os.path.dirname(chemin_csv)
        if dossier != "" and not os.path.exists(dossier):
            os.makedirs(dossier)
        lignes = []
        # on parcourt tous les documents du corpus
        for doc_id, doc in self.id2doc.items():
            #  fallback si get_type n'existe pas
            doc_type = doc.get_type() if hasattr(doc, "get_type") else "document"
            # champs spécifiques
            nb_comments = ""
            co_authors = ""
            # si reddit => on récupère nb_comments
            if doc_type == "reddit":
                nb_comments = doc.get_nb_comments()
            # si arxiv => on récupère la liste des co-auteurs
            elif doc_type == "arxiv":
                co_authors = ",".join(doc.get_co_authors())

            # on stocke une ligne dans le DataFrame
            lignes.append({
                "id": doc_id,
                "type": doc_type,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte,
                "nb_comments": nb_comments,
                "co_authors": co_authors
            })
        # transformation en DataFrame
        df = pd.DataFrame(lignes)
        # sauvegarde CSV (séparateur ';' pour Excel fr, même si l'énoncé exige la tabulation \t)
        df.to_csv(chemin_csv, sep=";", index=False, encoding="utf-8-sig")
    @classmethod
    def load(cls, chemin_csv, nom="corpus_charge"):
        # charge un corpus depuis un CSV
        # on récupère l'objet singleton
        corpus = cls(nom)
        # reset pour repartir d'un corpus vide
        corpus.nom = nom
        corpus.authors = {}
        corpus.id2doc = {}
        corpus.ndoc = 0
        corpus.naut = 0
        # lecture du fichier CSV
        df = pd.read_csv(chemin_csv, sep=";", encoding="utf-8-sig")
        # on parcourt chaque ligne du CSV
        for _, row in df.iterrows():
            # type du document
            doc_type = str(row.get("type", "document"))
            # création du document avec la factory
            doc = DocumentFactory.create(
                doc_type,
                titre=str(row.get("titre", "")),
                auteur=str(row.get("auteur", "")),
                date=str(row.get("date", "")),
                url=str(row.get("url", "")),
                texte=str(row.get("texte", "")),
                nb_comments=row.get("nb_comments", 0),
                co_authors=str(row.get("co_authors", ""))
            )
            # ajout dans le corpus
            corpus.add_document(doc)
        return corpus
