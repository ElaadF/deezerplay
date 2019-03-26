import numpy as np
import random
from keras.models import Sequential, Model
from keras.layers import Embedding, Reshape, Activation, Input, Dense
from keras.layers.merge import Dot
from keras.preprocessing.sequence import skipgrams
from sklearn.metrics import pairwise_distances
from sklearn.neighbors import KDTree
from operator import itemgetter
import pandas as pd


pl = "./resources/music_2.npy"
track_path = "./resources/./Tracks.csv"
data = np.load(pl)
playlist_track = [list(filter(lambda w: w.split("_")[0] == u"track", playlist)) for playlist in data]
tracks = np.unique(np.concatenate(playlist_track))
Vt = len(tracks)
track_counts = dict((tracks[i],0) for i in range(0, Vt))
for p in playlist_track:
    for a in p:
        track_counts[a]=track_counts[a]+1;

playlist_track_filter = [list(filter(lambda a : track_counts[a]> 7, playlist)) for playlist in playlist_track]
track_f = np.unique(np.concatenate(playlist_track_filter))
Vt = len(track_f)

track_dict = dict((track_f[i],i) for i in range(0, Vt))
# conversion des playlisat en liste d'entier
corpus_num_track = [[track_dict[track] for track in play ] for play in playlist_track_filter]

# hyper-paramètres de word2vec :
# dimension de l'espace latent
vector_dim = 50
# taille de la fenêtre de voisinage
window_width = 5
# sur-échantillonage des exemples négatifs
neg_sample = 4.
# taille des mini-batch
min_batch_size = 50
# coeff pour la loi de tirage des exemple negatif
samp_coef = -0.1

# comptage du nombre d'occurences des morceaux dans les playlist filtrées
tracks_counts_f = dict((track_f[i],0) for i in range(0, Vt))
for p in playlist_track_filter:
    for t in p:
        tracks_counts_f[t]=tracks_counts_f[t]+1;
# construction de la table de tirage des morceaux pour les exmeple negatif en utilisant ces fréquences
spt_tracks=np.array(list(map(lambda a:tracks_counts_f[a],track_f)),np.float)
sptn_tracks=np.power(spt_tracks,samp_coef)
sptn_tracks=sptn_tracks/np.sum(sptn_tracks)
sptn_tracks=np.cumsum(np.sort(sptn_tracks)[::-1])

# entrée deux entier (couple de morceaux)
input_target_t = Input((1,), dtype='int32')
input_context_t = Input((1,), dtype='int32')

# définition de l'embeding
embedding_t_t = Embedding(Vt, vector_dim, input_length=1, name='embedding_t')
# projection du premier morceau
target_t = embedding_t_t(input_target_t)
target_t = Reshape((vector_dim, 1))(target_t)

# projection du second morceaux
context_t = embedding_t_t(input_context_t)
context_t = Reshape((vector_dim, 1))(context_t)

# calcul de la sortie
dot_product_t = Dot(axes=0)([target_t, context_t])
dot_product_t = Reshape((1,))(dot_product_t)
output_t = Dense(1, activation='sigmoid',name="classif")(dot_product_t)

# definition du modèle
SkipGram_t = Model(inputs=[input_target_t, input_context_t], outputs=output_t)
SkipGram_t.compile(loss='binary_crossentropy', optimizer='adam')

def track_ns_generator(corpus_num,nbm):
    while 1:
        Data=[]
        Labels=[]
        for i, doc in enumerate(random.sample(corpus_num,nbm)):
            data, labels = skipgrams(sequence=doc, vocabulary_size=Vt, window_size=window_width, negative_samples=neg_sample,sampling_table=sptn_tracks)
            if (len(data)>0):
                Data.append(np.array(data, dtype=np.int32))
                Labels.append(np.array(labels, dtype=np.int32))
        Data=np.concatenate(Data)
        Labels=np.concatenate(Labels)
        x=[Data[:,0],Data[:,1]]
        y=Labels
        yield (x,y)


index_tst = np.random.choice(100000,10000)
index_app  = np.setdiff1d(range(100000),index_tst)

play_app   = [corpus_num_track[i] for i in index_app]
play_tst  = [corpus_num_track[i] for i in index_tst]

hist=SkipGram_t.fit_generator(track_ns_generator(play_app,min_batch_size),200,5)

# récupérations des positions des morceaux dans l'espace de projection
vectors_tracks = SkipGram_t.get_weights()[0]

def predict(seeds,s,X, metric='euclidean'):
    V = X.shape[0]
    others = np.setdiff1d(range(V),seeds)
    D = pairwise_distances(X[seeds,:],X[others,:],metric)
    return others[np.argsort(np.min(D,0))[:s]]

#pr=predict([0,1],4,vectors_tracks)

def test_pairwise(metrics='euclidean'):
    # nombre de bonne prediction
    goodpred = []
    # nombre de predictions faites
    nbpred   = []
    # pour chaque playlist
    for p in play_tst:
        # si au moins deux chansons
        if (len(p)>1):
            # recuperations des seeds 5 premiers morceaux ou moins si la playlist contient moins de 5 morceaux
            seeds  = p[:np.min([5,len(p)-1])]
            # recuperations de la suite de la playlist que nous allons comparer à nos suggestions
            topred = p[np.min([5,len(p)-1]):]
            # construction des suggestions 10 suggestions par morceaux a predire
            prediction = predict(seeds,10*len(topred),vectors_tracks, metrics)
            # comptage du nombre de morceaux présent dans nos suggestions
            goodpred.append(len(np.intersect1d(prediction,topred)))
            # stockage du nombre de predictions
            nbpred.append(len(topred))
    # proportions de morceux présents dans nos suggestions
    return np.sum(goodpred)/np.sum(nbpred)

tr_meta=pd.read_csv(track_path)
jdf = pd.DataFrame({"id":track_f,"index":range(Vt)})
jdf["deezer_id"]=jdf["id"].apply(lambda x: float(x.split("_")[1]))

trj_meta = tr_meta.merge(jdf, left_on="id",right_on="deezer_id")
trj_meta.set_index("index",inplace=True)

kdt = KDTree(vectors_tracks, leaf_size=30, metric='euclidean')


def predict_opt(seeds, s, X, kdt):
    V = X.shape[0]
    seeds_size = len(seeds)
    others = np.setdiff1d(range(V), seeds)

    dist, ind = kdt.query(X[seeds, :], k=s + seeds_size)
    dist_ind_list = np.concatenate(np.dstack((dist, ind)))
    dist_ind_list2 = list(map(lambda x: tuple(x), dist_ind_list))
    sorted_dist_ind_list = sorted(dist_ind_list2, key=itemgetter(0))[seeds_size: (s + seeds_size)]

    neigh = list(map(lambda x: x[1], sorted_dist_ind_list))
    return neigh

#pr2=predict_opt([0,1],25,vectors_tracks, kdt)

def test_predict_opt(leaf_size=10, metric='euclidean'):
    kdt = KDTree(vectors_tracks, leaf_size, metric)
    # nombre de bonne prediction
    goodpred = []
    # nombre de predictions faites
    nbpred = []
    # pour chaque playlist
    for p in play_tst:
        # si au moins deux chansons
        if (len(p) > 1):
            seeds = p[:np.min([5, len(p) - 1])]
            topred = p[np.min([5, len(p) - 1]):]

            prediction = predict_opt(seeds, 10 * len(topred), vectors_tracks, kdt)
            goodpred.append(len(np.intersect1d(prediction, topred)))
            nbpred.append(len(topred))

    return np.sum(goodpred) / np.sum(nbpred)



def pred_list(seeds):
    pr = predict_opt(seeds,25,vectors_tracks,kdt)
    return trj_meta.loc(pr,["titre","artist","preview","album"]).values

def all_list():
    return trj_meta[["title","artist","preview","album"]].values








