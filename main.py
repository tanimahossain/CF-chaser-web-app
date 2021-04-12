
import cfapi_handler
import problem_recommender

def profile_varification():
	user_name = input("username -- ")

	profile = cfapi_handler.user_profile(user_name)

	if "name" not in profile:
		print("user doesnt exist.")
	else:
		print("user exist.")


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
	user_name = input("username -- ")
	data = cfapi_handler.contest_participation(user_name)
	for i in data:
		print(i)

def contest_solve():
	user_name = input("username -- ")
	contest_id = input("contest id -- ")
	data = cfapi_handler.contest_solve(user_name, contest_id)
	print(data)



def recommend():
	username = input("username -- ")
	data = problem_recommender.recommender(username)
	for i in data:
		print(i)

recommend()
