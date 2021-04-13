import urllib
from urllib.request import urlopen as Ureq, Request
import json
import time

hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def get_json(url):
	try:
		req = Request(url, headers=hdr)
		page = Ureq(req)
	except:
		return None

	try:
		js = page.read().decode()
		js = json.loads(js)
	except:
		return None

	return js

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def user_profile(username):
	url = "https://codeforces.com/api/user.info?handles="
	url += username
	js = get_json(url)
	ret = {}

	if not js or "status" not in js or js["status"] != "OK":
		return ret
	js = js["result"][0]

	try:
		ret["name"] = js["firstName"] + " " + js["lastName"];
		ret["handle"] = js["handle"];
		ret["organization"] = js["organization"];
		ret["max_rating"] = js["maxRating"];	
		ret["max_rank"] = js["maxRank"];
		ret["cur_rating"] = js["rating"];
		ret["cur_rank"] = js["rank"];
		ret["friend_of"] = js["friendOfCount"];
		ret["address"] = js["city"] + ", " + js["country"];
		ret["profile_picture"] = js["titlePhoto"];
		ret["country"] = js["country"]
	except:
		return {}

	return ret;


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def current_population():
	url = "https://codeforces.com/api/user.ratedList?activeOnly=true"
	js = get_json(url)
	ret = {}
	if not js or "status" not in js or js["status"] != "OK":
		return ret
	for user in js["result"]:
		ret[user["rank"]] = ret.get(user["rank"], 0) + 1;
	return ret

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def recent_performance(username, last_x_day):
	last_x_day = int(last_x_day)
	url = "https://codeforces.com/api/user.status?handle="
	url += username
	js = get_json(url)
	ret = {}
	if not js or "status" not in js or js["status"] != "OK":
		return ret

	taken = set()
	prob_tags = set()
	total_rating_solved = 0
	time_lim = time.time() - (last_x_day*24*60*60);
	ret["unrated"] = ret["A"] = ret["B"] = ret["C"] = ret["D"] = ret["E"] = ret["F"] = 0
	
	for submission in js["result"]:
		if submission["verdict"] != "OK":
			continue
		if submission["creationTimeSeconds"] < time_lim:
			break
		prob_id = str(submission["problem"]["contestId"]) + submission["problem"]["index"]
		if prob_id in taken:
			continue
		taken.add(prob_id)
		try:
			rating = submission["problem"]["rating"]
			total_rating_solved += rating
		except:
			rating = -1
		if rating == -1:
			ret["unrated"] += 1;
		elif rating <= 1000:
			ret["A"] += 1;
		elif rating <= 1500:
			ret["B"] += 1;
		elif rating <= 2000:
			ret["C"] += 1;
		elif rating <= 2500:
			ret["D"] += 1;
		elif rating <= 3000:
			ret["E"] += 1;
		else:
			ret["F"] += 1;
		tags = submission["problem"]["tags"]
		for tag in tags:
			prob_tags.add(tag)
	
	ret["topic_solved"] = list(prob_tags)
	ret["performance_point"] = total_rating_solved / (last_x_day * 24)
	return ret


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def contest_participation(username):
	url = "https://codeforces.com/api/user.status?handle="
	url += username
	js = get_json(url)

	if not js or "status" not in js or js["status"] != "OK":
		return []
	contest_id = set()

	for submission in js["result"]:
		contest_id.add(submission["contestId"])
	
	contest_id = list(contest_id)
	contest_id.sort()

	return [str(x) for x in contest_id]

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def contest_solve(username, contest_id):
	url = "https://codeforces.com/api/contest.status?contestId=" + contest_id + "&handle=" + username
	js = get_json(url)
	if not js or "status" not in js or js["status"] != "OK":
		return []
	ac_prob = set()
	
	for submission in js["result"]:
		if submission["verdict"] == "OK":
			if submission["problem"]["index"] not in ac_prob:
				ac_prob.add(submission["problem"]["index"])
	return sorted(list(ac_prob))

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
