
import cfapi_handler
import problem_recommender

def profile_varification():
	user_name = input("usernames e.g. 'strange_r ah_med' -- ")
	user_name = user_name.split()

	profile = cfapi_handler.user_profile(user_name)

	print("-----------------------------------")
	print("---------- Profile Data -----------")
	print("-----------------------------------")
	for (i, j) in profile.items():
		print(i,"\n")
		for (k, l) in j.items():
			print(k," : ", l)
		print("-----------------------------------\n")


def population_check():
	pop = cfapi_handler.current_population()
	for (i, j) in pop.items():
		print(i, j)


def recent_performance():
	user_name = input("username -- ")
	day = input("last x day -- ")

	data = cfapi_handler.recent_performance(user_name, day)
	for (i, j) in data.items():
		print(i, j)

def contest_perticipation():
	data = cfapi_handler.contest_participation(["strange_r", "ah_med", "el.duivel","erfanul007","gHo0sT"])	

	print("------------------------------------------")
	for (cid, cdata) in data.items():
		print(cid, " : ", cdata["name"]);

		for (user, solve) in cdata["user"].items():
			print(user, " : ", solve);
		print("------------------------------------------")

def recommend():
	username = input("username -- ")
	data = problem_recommender.recommender(username)
	for i in data:
		print(i)

contest_perticipation()

