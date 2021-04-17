import urllib
from urllib.request import urlopen as Ureq, Request
import json
import time
import random

hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

def get_json(url):
	req = Request(url, headers=hdr)
	page = Ureq(req)
	try:
		js = page.read().decode()
		js = json.loads(js)
	except:
		js = None
	return js

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

user_solve = set()

def get_user_solve(username):
	url = "https://codeforces.com/api/user.status?handle=" + username

	js = get_json(url)
	if not js or "status" not in js or js["status"] != "OK":
		return

	for submission in js["result"]:
		if submission["verdict"] == "OK":
			user_solve.add(str(submission["problem"]["contestId"])+submission["problem"]["index"])

contest_list = set()

def get_contest_list():
	url = "https://codeforces.com/api/contest.list"

	js = get_json(url)
	if not js or "status" not in js or js["status"] != "OK":
		return

	for contest in js["result"]:
		name = contest["name"]
		if "Div" in name:
			contest_list.add(contest["id"])

def get_user_rating(username):
	url = "https://codeforces.com/api/user.info?handles=" + username
	js = get_json(url)
	
	if not js or "status" not in js or js["status"] != "OK":
		return 600
	js = js["result"][0]

	try:
		return js["rating"];
	except:
		return 600

def not_taken(ls, tags):
	mx = 0
	for i in ls:
		cnt = 0;
		for j in i[2]:
			if j in tags:
				cnt += 1
		try:
			per =  (cnt / len(i[2])) * 100;
		except:
			return False
		mx = max(mx, per)
	if mx > 80 and len(tags) == 0:
		return False
	return True


def recommender(username):
	username = username.split()
	user_rating = get_user_rating(username[0])
	if user_rating is None:
		return []
	user_rating = int(user_rating / 100)
	user_rating = int(user_rating * 100)

	for user in username:
		get_user_solve(user)
	get_contest_list()

	url = "https://codeforces.com/api/problemset.problems"
	js = get_json(url)

	if not js or "status" not in js or js["status"] != "OK":
		return []

	ret = list()
	prob_a = 0
	prob_b = 0
	prob_c = 0
	js = js["result"]["problems"]
	random.shuffle(js)

	for problem in js:
		link = "https://codeforces.com/contest/" + str(problem["contestId"]) + "/problem/" + problem["index"]
		name = problem["name"]
		try:
			rating = problem["rating"]
		except:
			continue
		tags = problem["tags"]
		contest_id = problem["contestId"]

		prob_id = str(problem["contestId"]) + problem["index"]
		if prob_id not in user_solve and contest_id in contest_list:

			if rating == user_rating+100 and prob_a < 2:
				if not_taken(ret, tags):
					ret.append([link, name, tags, rating])
					prob_a += 1
			elif rating == user_rating+200 and prob_b < 2:
				if not_taken(ret, tags):
					ret.append([link, name, tags, rating])
					prob_b += 1
			elif rating == user_rating+300 and prob_c < 6:
				if not_taken(ret, tags):
					ret.append([link, name, tags, rating])
					prob_c += 1

		if len(ret) >= 10:
			return ret;
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

