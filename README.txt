Projet Python : VERSION1 TD3 à TD5*
Binômes: Fatine MOURID & Manel SAADANE
Programmation de spécialité (Python)

Objectif
Ce projet a pour but de mettre en place un moteur de recherche d’information simplifié, sans utiliser de bibliothèques prêtes à l’emploi, à partir de données textuelles provenant de Reddit et d’ArXiv.

Contenu du projet
- TD3 : acquisition des données, sauvegarde et premières statistiques
- TD4 : structuration du code avec des classes (Document, Author, Corpus)
- TD5 : héritage, polymorphisme et patrons de conception (Factory, Singleton)

Organisation des fichiers
- main.py : script principal d’exécution
- TD3_recuperation_reddit.py : récupération des données Reddit
- TD3_recuperation_arxiv.py : récupération des données ArXiv
- TD3_corpus_io.py : création et sauvegarde du DataFrame
- TD3_stats.py : statistiques simples sur le corpus
- TD4_5_document.py : classes Document, RedditDocument et ArxivDocument
- TD4_5_author.py : classe Author
- TD4_5_corpus.py : classe Corpus + sauvegarde/chargement + patrons

Exécution
Lancer le script principal avec la commande suivante :
python main.py

Prérequis
Les bibliothèques nécessaires :
praw: python -m pip install praw pandas xmltodict, python -m pip install praw
pandas
xmltodict