from surprise import Dataset
from surprise import Reader
from surprise.model_selection import GridSearchCV, cross_validate
import pandas as pd
from surprise import dump
import os
from collections import defaultdict
from surprise import KNNWithMeans, KNNBasic, KNNWithZScore, KNNBaseline, SVD, SVDpp, NMF

msd_data = None
mapping = None
clusters = None
to_update_song = {}
to_update_cluster = {}
songs_to_clusters = {}

def get_top_n(predictions, n, mode):
    # First map the predictions to each user.
    global to_update_song
    global to_update_cluster
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        if mode == "cluster_id":
            if uid in to_update_cluster:
                for item in to_update_cluster[uid]:
                    if item[0] == iid:
                        top_n[uid].append((iid, item[1]))
                        seen = True
                    else:
                        top_n[uid].append((iid, est))
                for items in to_update_cluster[uid]:
                    top_n[uid].append((items[0], items[1]))
            else:
                top_n[uid].append((iid, est))
            to_update_cluster = {}
        else:
            if uid in to_update_song:
                for item in to_update_song[uid]:
                    if item[0] == iid:
                        top_n[uid].append((iid, item[1]))
                    else:
                        top_n[uid].append((iid, est))
            else:
                top_n[uid].append((iid, est))
            to_update_song = {}

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

def load_data(path):
    global msd_data
    global clusters
    global mapping
    common_title_set = pd.read_csv(path + "fma_msd_title_intersection.csv")['0']
    msd_data = pd.read_csv(path + "msd_tuples.csv")
    m = msd_data.song_name.isin(common_title_set)
    msd_data = msd_data[m]
    msd_data = msd_data[["user_id", "song_name", "play_count"]][:10000]
    cluster_data = pd.read_csv(path + "tracks_8_clusters.csv")
    clusters = msd_data.merge(cluster_data, left_on='song_name', right_on='track_title', how='left', indicator=True)
    mapping = clusters[["song_name", "cluster_id"]]
    mapping = mapping.set_index('song_name').to_dict()['cluster_id']

def write_data():
    users = msd_data['user_id']
    users.drop_duplicates().to_csv("users.csv")
    songs = msd_data['song_id']
    songs.drop_duplicates().to_csv("songs.csv")

def retrain(mode):
    # mode should be song_name or cluster_id
    global msd_data
    global clusters
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(clusters[["user_id", mode, "play_count"]], reader)
    trainset = data.build_full_trainset()
    # train model
    model = KNNWithMeans()
    model.fit(trainset)
    file_name = os.path.expanduser('model_file_' + mode)
    dump.dump(file_name, algo=model)
    _, loaded_algo = dump.load(file_name)

    testset = trainset.build_anti_testset()
    predictions = loaded_algo.test(testset)
    if mode == 'song_name':
        top_n = get_top_n(predictions, 10, mode)
    else:
        top_n = get_top_n(predictions, 1, mode)
    pd.DataFrame(top_n).to_csv("predictions_" + mode + ".csv")

def update_recommendations(user, song, rating, mode, do_retrain=False):
    global to_update_song
    global to_update_cluster
    if mode == "cluster_id":
        if user in to_update_cluster:
            to_update_cluster[user] += [(mapping[song], rating)]
        else:
            to_update_cluster[user] = [[mapping[song], rating]]
    else:
        if user in to_update_song:
            to_update_song[user] += [(song, rating)]
        else:
            to_update_song[user] = [[song, rating]]
    if do_retrain:
        retrain(mode)
    
def get_predictions_for_user(user_id, mode):
    predictions = pd.read_csv("predictions_" + mode + ".csv")
    result = []
    for pred in predictions[user_id]:
        title, rating = pred.split(",")
        title = title.replace(")","").replace("(","").replace("'","")
        rating = rating.replace(")","").replace("(","").replace(" ","")
        if mode == 'song_name':
            result += [[title, mapping[title], float(rating)]]
        else:
            result += [[title, float(rating)]]
    return result