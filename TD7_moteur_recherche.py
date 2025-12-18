# TD7 : implémentation d'un moteur de recherche
import numpy as np  # calculs numériques
import pandas as pd  # tableau de résultats
from scipy.sparse import csr_matrix  # matrice creuse (conseillée)
from td6_traitement_texte import tokenize  # découper le texte en mots
from tqdm import tqdm
class SearchEngine:  # classe demandée dans l'énoncé
    def __init__(self, corpus):  # on passe un Corpus au moteur
        self.corpus = corpus  # on garde le corpus
        self.N = len(self.corpus.id2doc)  # nombre de documents
        self.vocab = {}  # dictionnaire vocab (mot : infos)
        self.terms = []  # liste des mots triés
        self.mat_TF = None  # matrice Documents x Terms en TF
        self.mat_TFIDF = None  # matrice Documents x Terms en TF-IDF
        self.doc_norms_TF = None  # normes des docs en TF (cosinus)
        self.doc_norms_TFIDF = None  # normes des docs en TF-IDF (cosinus)
        self.build()  # on construit tout dès le début
    def build(self):  # Partie 1 : construire vocab et matrices
        docs = []  # liste des textes
        for doc in self.corpus.id2doc.values():  # parcourir les documents
            docs.append(str(doc.texte))  # ajouter le texte
        vocab_set = set()  # set pour enlever les doublons
        for txt in docs:  # parcourir chaque texte
            for w in tokenize(txt):  # découper en mots
                if w != "":  # ignorer vide
                    vocab_set.add(w)  # ajouter au vocab
        self.terms = sorted(vocab_set)  # trier par ordre alphabétique
        for j, w in enumerate(self.terms):  # donner un index à chaque mot
            self.vocab[w] = {"index": j, "tf_total": 0, "df": 0}  # infos du mot
        rows = []  # indices ligne (document)
        cols = []  # indices colonne (mot)
        data = []  # valeurs TF
        for i, txt in tqdm(list(enumerate(docs)), total=len(docs)):# i = index du document
            counts = {}  # compteur TF pour ce document
            for w in tokenize(txt):  # parcourir les mots
                if w in self.vocab:  # si mot connu
                    j = self.vocab[w]["index"]  # index du mot
                    counts[j] = counts.get(j, 0) + 1  # +1 occurrence
            for j, tf in counts.items():  # remplir la matrice
                rows.append(i)  # ligne doc
                cols.append(j)  # colonne mot
                data.append(float(tf))  # valeur TF
        self.mat_TF = csr_matrix(  # matrice Documents x Terms
            (data, (rows, cols)),  # format sparse
            shape=(self.N, len(self.terms)),  # dimension
            dtype=float  # type float
        )
        tf_total = np.asarray(self.mat_TF.sum(axis=0)).ravel()  # total occurrences par mot
        df = np.asarray((self.mat_TF > 0).sum(axis=0)).ravel().astype(int)  # nb docs contenant le mot
        for j, w in enumerate(self.terms):  # stocker ces infos dans vocab
            self.vocab[w]["tf_total"] = int(tf_total[j])  # total corpus
            self.vocab[w]["df"] = int(df[j])  # document frequency
        self.mat_TFIDF = self.compute_tfidf(self.mat_TF, df)  # matrice TF-IDF
        self.doc_norms_TF = self.row_norms(self.mat_TF)  # normes pour cosinus TF
        self.doc_norms_TFIDF = self.row_norms(self.mat_TFIDF)  # normes pour cosinus TF-IDF
    def compute_tfidf(self, mat_tf, df):  # TF-IDF
        df_safe = np.where(df == 0, 1, df)  # éviter division par 0
        idf = np.log(self.N / df_safe)  # IDF = log(N/df)
        idf_row = csr_matrix(idf.reshape(1, -1))  # transformer en 1xV
        return mat_tf.multiply(idf_row)  # TF * IDF
    def row_norms(self, mat):  # norme euclidienne par document
        sq = mat.multiply(mat).sum(axis=1)  # somme des carrés
        return np.sqrt(np.asarray(sq)).ravel()  # racine carrée
    def vectorize_query(self, mots_cles, use_tfidf=True):  # transformer requête en vecteur
        tokens = tokenize(mots_cles)  # découper la requête
        if len(tokens) == 0:  # requête vide
            return csr_matrix((1, len(self.terms)), dtype=float)  # vecteur vide
        counts = {}  # compteur TF de la requête
        for w in tokens:  # parcourir les mots
            if w in self.vocab:  # si le mot est dans le vocab
                j = self.vocab[w]["index"]  # index du mot
                counts[j] = counts.get(j, 0) + 1  # compter
        if len(counts) == 0:  # aucun mot trouvé dans vocab
            return csr_matrix((1, len(self.terms)), dtype=float)  # vecteur vide
        rows = [] # toujours 0 pour la requête
        cols = [] # indices des mots
        data = [] # valeurs TF
        for j, tf in counts.items():  # construire le vecteur sparse
            rows.append(0)  # une seule ligne
            cols.append(j)  # colonne mot
            data.append(float(tf))  # TF requête
        q_tf = csr_matrix((data, (rows, cols)), shape=(1, len(self.terms)), dtype=float)  # vecteur requête TF
        if not use_tfidf:  # si on veut TF simple
            return q_tf  # retourner TF
        df = np.array([self.vocab[w]["df"] for w in self.terms], dtype=int)  # df du corpus
        df_safe = np.where(df == 0, 1, df)  # éviter 0
        idf = np.log(self.N / df_safe)  # même IDF que corpus
        idf_row = csr_matrix(idf.reshape(1, -1))  # 1xV
        return q_tf.multiply(idf_row)  # requête en TF-IDF
    def cosine_scores(self, mat_docs, doc_norms, q_vec):  # similarité cosinus
        q_norm = float(np.sqrt(q_vec.multiply(q_vec).sum()))  # norme requête
        if q_norm == 0:  # si vecteur vide
            return np.zeros(self.N)  # scores nuls
        num = (mat_docs @ q_vec.T).toarray().ravel()  # produit scalaire docs·requête
        den = doc_norms * q_norm  # dénominateur
        den = np.where(den == 0, 1e-12, den)  # éviter division par 0
        return num / den  # cosinus
    def search(self, mots_cles, nb_docs=5, use_tfidf=True):  # Partie 2 & 3 : fonction search
        q_vec = self.vectorize_query(mots_cles, use_tfidf=use_tfidf)  # vecteur requête
        if use_tfidf:  # si TF-IDF
            scores = self.cosine_scores(self.mat_TFIDF, self.doc_norms_TFIDF, q_vec) # scores TF-IDF
        else:  # sinon TF
            scores = self.cosine_scores(self.mat_TF, self.doc_norms_TF, q_vec)  # scores TF
        top = np.argsort(scores)[::-1][:nb_docs]  # trier et garder les meilleurs
        lignes = []  # lignes du résultat
        for i in top:  # parcourir meilleurs docs
            doc = self.corpus.id2doc[i]  # récupérer document
            lignes.append({  # ajouter ligne
                "doc_id": i,  # id doc
                "score": float(scores[i]),  # score
                "titre": doc.titre,  # titre
                "auteur": doc.auteur,  # auteur
                "date": doc.date,  # date
                "url": doc.url  # url
            })
        return pd.DataFrame(lignes)  # l'énoncé demande un DataFrame
