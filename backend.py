import pandas as pd
from sklearn.cluster import KMeans
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

users = {}
active_user = None

class User():
	def __init__(self, username):
		self.name = username
		self.listened_tracks = {} # {track_title : (play_count, rating), ...}

def init():
	global tracks_8_clusters
	global tracks_16_clusters

	tracks_8_clusters = pd.read_csv(PATH_CL_8, index_col=0)
	tracks_16_clusters = pd.read_csv(PATH_CL_16, index_col=0)

	print(tracks_8_clusters.head())
	print(tracks_16_clusters.head())


def get_user():
	global active_user
	return active_user


def login(username):
	global active_user

	if username not in users:
		user = User(username)
		users[username] = user

		active_user = user
	else:
		active_user = users[username]


def logout():
	active_user = None


def log_rating(track_title, rating):
	if active_user is None:
		print("You must log in")
		return
	
	if track_title not in active_user.listened_tracks:
		active_user.listened_tracks[track_title] = (1, rating)
	else:
		active_user.listened_tracks[track_title] = (active_user.listened_tracks[track_title][0] + 1, rating)


def get_recommendation():
	if active_user is None:
		print("You must log in")
		return

	return ['track_title_1', 'track_title_2']


def update_recommendation():
	pass


init()
