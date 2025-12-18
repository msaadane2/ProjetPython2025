# Projet Python : RENDU FINAL TD3 au TD10
# Binômes: Fatine MOURID & Manel SAADANE
# Programmation de spécialité (Python)

# Objectif
Ce projet a pour but de mettre en place un moteur de recherche d’information simplifié, sans utiliser de bibliothèques prêtes à l’emploi, à partir de données textuelles provenant de Reddit et d’ArXiv.

# Contenu du projet
- TD3 : acquisition des données, sauvegarde et premières statistiques
- TD4 : structuration du code avec des classes (Document, Author, Corpus)
- TD5 : héritage, polymorphisme et patrons de conception (Factory, Singleton)
- TD6 : Analyse du contenu textuel
- TD7: Moteur de recherche 
- TD8 : intégration du moteur avec une interface à partir d’un fichier CSV
- TD9/10: Mini-projet: interface utilisateur 

# Organisation des fichiers
- discours_US.csv : jeu de données textuelles
- main.py : script principal d’exécution
- TD3_recuperation_reddit.py : récupération des données Reddit
- TD3_recuperation_arxiv.py : récupération des données ArXiv
- TD3_corpus_io.py : création et sauvegarde du DataFrame
- TD3_stats.py : statistiques simples sur le corpus
- TD4_5_document.py : classes Document, RedditDocument et ArxivDocument
- TD4_5_author.py : classe Author
- TD4_5_corpus.py : classe Corpus + sauvegarde/chargement + patrons
- td6_traitement_texte: Traitement du texte
- TD7_moteur_recherche: Moteur de recherche
- td8_core.py : construction du moteur à partir d’un fichier CSV
- app.py : interface graphique Streamlit pour td8 et pour mini projet
- td8_interface.ipynb : notebook Jupyter pour le TD8
- td9_10_InterfaceCorpus.ipynb : notebook Jupyter pour le TD9–TD10

# Précision T8/9/10: 
Les TD8, TD9 et TD10 ont été initialement développés dans un environnement Anaconda, en utilisant Jupyter Notebook (.ipynb) afin de faciliter l’exploration des données, les tests progressifs et la mise au point des différentes fonctionnalités.
Dans une étape suivante, les notebooks Jupyter ont été exportés en scripts Python (.py). Le code obtenu a ensuite été réorganisé et intégré dans une nouvelle interface développée en Python avec la bibliothèque Streamlit.
Cette interface Streamlit reprend la même logique et les mêmes fonctionnalités que celles implémentées dans les fichiers .ipynb, avec en plus une exécution standardisée et interactive via un navigateur web.
Cette transition permet :
- de conserver le travail réalisé dans les notebooks,
- d’obtenir une version exécutable et modulaire du projet

Les fichiers .ipynb sont donc conservés comme support de développement, tandis que les fichiers .py et l’interface Streamlit constituent la version finale du projet.

# Prérequis système
Python 

# Exécution
Lancer le script principal avec la commande suivante :
python main.py

# Les bibliothèques nécessaires :
- pandas – manipulation des données tabulaires
- praw – récupération des données depuis Reddit
- xmltodict – parsing des données XML de l’API arXiv
- scipy – matrices creuses et calculs numériques (TF / TF-IDF)
- tqdm – barre de progression pour les traitements longs
- streamlit – interface graphique interactive (TD8 à TD10)
- ipywidgets – utilisé lors du prototypage sous Jupyter Notebook

# Installation recommandée :
pip install pandas praw xmltodict scipy tqdm streamlit ipywidgets
pip install streamlit
