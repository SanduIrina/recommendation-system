import os
from backend import *


Actions = """
Choose actions:
 1. logout
 2. get_recommendations
 3. give rating
 4. change recommendation mode
 5. recompute recommendations
 6. exit
: """

Modes = """
Choose modes:
 1. songs
 2. clusters
: """

Login = """
Users:
  Mihai
  Irina
  Andreea
  Bob
  Baker
  Ion
Please log in: """

def run():
	mode = "cluster_id"
	mapping = get_mapping()

	while True:
		active_user = get_user()
		# os.system('cls' if os.name=='nt' else 'clear')

		if active_user is None:
			username = input(Login)

			ret = login(username)

			if ret == -1:
				continue

		action = input(Actions)

		if action in ["1.", "1", "logout"]:
			logout()
			active_user = None
		elif action in ["2.", "2", "get_recommendations", "get recommendations"]:
			songs = get_recommendation(mode)

			print("Recommendation mode: %s" % mode)
			print("Recommended songs: ")

			for song in songs:
				print("%d\t%s" % (0, song))
		elif action in ["3.", "3", "give_rating", "give rating"]:
			track_title = input("Enter track title: ")
			rating = input("Enter rating: ")

			try:
				rating = int(rating)

				log_rating(track_title, rating, mode)
			except:
				print("Enter a valid track and rating!")
		elif action in ["4.", "4", "change recommendation mode"]:
			mode = input(Modes)
			if mode in ["1.", "1", "songs"]:
				mode = "song_name"
			else:
				mode = "cluster_id"
		elif action in ["5.", "5", "recompute recommendations"]:
			update_recommendation(mode)
		elif action in ["6.", "6", "exit"]:
			break



if __name__ == '__main__':
	run()
