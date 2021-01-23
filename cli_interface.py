import os
from backend import active_user, login, get_user


HELP = """

"""


def run():
	

	print(HELP)

	while True:
		active_user = get_user()
		# os.system('cls' if os.name=='nt' else 'clear')

		if active_user is None:
			print("Please log in:")
			username = input()

			login(username)
		else:
			break



if __name__ == '__main__':
	run()
