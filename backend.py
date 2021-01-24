import pandas as pd
import random
from sklearn.cluster import KMeans
import sys
sys.path.append('collab-filtering/')
from predict import *

#from irina import send_recommendation, update_recommendation

def send_recommendation(username):
	return [
	('track1', 0, 1),
	('track2', 0, 2),
	('track3', 0, 3),
	('track4', 0, 4),
	('track5', 0, 5),
	]

def update_recommendation(rating_tuples):
	pass

PATH_CL_8 = "./clustered-tracks/tracks_8_clusters.csv"
PATH_CL_16 = "./clustered-tracks/tracks_16_clusters.csv"

tracks_8_clusters = None
tracks_16_clusters = None

user_ids = {
	"Mihai" :	 "b80344d063b5ccb3212f76538f3d9e43d87dca9e",
	"Irina" :	 "6d50e6ffc091a51d1cec5a91c2fe78d1939ed980",
	"Andreea" :	 "5e47421e4f42b4944be42f3d4a24bb71692e77e4",
	"Bob" :		 "e05f5b1dba3eece71df341b2b9160cf2e84bda39",
	"Baker" :	 "bdc7c976ce178aa4e75bbf9874fdaf327f3d3fe2",
	"Ion" :		 "079255bdeae163a2a66f9b9e33dc6e3f0e4e6dd7",
}
active_user = None

mapping = {}
inverse_mapping = {}

track_title_list = []


def init():
	global mapping
	global inverse_mapping
	global track_title_list

	load_data("collab-filtering/data/")
	mapping = get_mapping()

	for track_title, cluster_id in mapping.items():
		if cluster_id not in inverse_mapping:
			inverse_mapping[cluster_id] = [track_title]
		else:
			inverse_mapping[cluster_id].append(track_title)

	track_title_list = list(mapping.keys())


def get_user():
	global active_user
	return active_user


def get_inverse_mapping():
	global inverse_mapping
	return inverse_mapping


def login(username):
	global active_user

	if username not in user_ids:
		print("Not a valid user")
		return -1
	else:
		active_user = user_ids[username]
		return 0


def logout():
	global active_user
	active_user = None


def log_rating(track_title, rating, mode = "song_name"):
	if active_user is None:
		print("You must log in")
		return
	
	update_recommendation(user_ids[active_user], track_title, rating, mode, False)


def get_recommendation(mode):
	global track_title_list
	global inverse_mapping

	if active_user is None:
		print("You must log in")
		return

	songs = []

	if mode == "song_name":
		rec_songs = [x for x, _, _ in get_predictions_for_user(active_user, mode)]
		songs = random.choices(rec_songs, k = 5)

	else:
		cluster_id = get_predictions_for_user(active_user, mode)[0][0]

		songs = random.choices(inverse_mapping[int(cluster_id)], k = 5)


	rand_songs = random.choices(track_title_list, k = 5)
	songs.extend(rand_songs)
	return list(set(songs))


def update_recommendation(mode = "song_name"):
	retrain(mode)


init()
