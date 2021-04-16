import urllib
from urllib.request import urlopen as Ureq, Request
import json
import time

hdr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def get_json(url):
    try:
        req = Request(url, headers=hdr)
        page = Ureq(req)

        js = page.read().decode()
        js = json.loads(js)
    except:
        return None

    return js


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def user_profile(usernames):
    url = "https://codeforces.com/api/user.info?handles="
    url += usernames[0]
    for i in range(1, len(usernames)):
        url += str(";" + usernames[i])

    # print(url)

    js = get_json(url)

    if not js or "status" not in js or js["status"] != "OK":
        return {}

    ret = {}
    for user in usernames:
        ret[user] = {}

    js = js["result"]

    for profile in js:
        try:
            handle = profile["handle"]
            ret[handle]['handle'] = handle
        except:
            continue

        try:
            name = str(profile["firstName"] + " " + profile["lastName"]).title()
        except:
            name = ""
        ret[handle]["name"] = name

        try:
            organization = str(profile["organization"]).title()
        except:
            organization = ""
        ret[handle]["organization"] = organization

        try:
            max_rating = profile["maxRating"]
        except:
            max_rating = ""
        ret[handle]["max_rating"] = max_rating

        try:
            max_rank = str(profile["maxRank"]).title()
        except:
            max_rank = ""
        ret[handle]["max_rank"] = max_rank

        try:
            cur_rating = profile["rating"]
        except:
            cur_rating = ""
        ret[handle]["cur_rating"] = cur_rating

        try:
            cur_rank = str(profile["rank"]).title()
        except:
            cur_rank = ""
        ret[handle]["cur_rank"] = cur_rank

        try:
            friend_of = profile["friendOfCount"]
        except:
            friend_of = ""
        ret[handle]["friend_of"] = friend_of

        try:
            city = str(profile["city"]).title()
        except:
            city = ""
        ret[handle]["city"] = city

        try:
            country = str(profile["country"]).title()
        except:
            country = ""
        ret[handle]["country"] = country

        try:
            profile_picture = profile["titlePhoto"]
        except:
            profile_picture = ""
        ret[handle]["profile_picture"] = profile_picture

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
    time_lim = time.time() - (last_x_day * 24 * 60 * 60);
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

    ret["point_per_hour"] = str(total_rating_solved / (last_x_day * 24))
    ret["topic_solved"] = list(prob_tags)
    return ret


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def get_valid_contest_list():
    url = "https://codeforces.com/api/contest.list"

    js = get_json(url)
    if not js or "status" not in js or js["status"] != "OK":
        return set()

    contest_list = {}

    for contest in js["result"]:
        name = contest["name"]
        cid = contest["id"]
        if "Div" in name:
            contest_list[cid] = name

    return contest_list


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def contest_participation(usernames):
    contest_list = get_valid_contest_list()
    valid_contest = set();
    for i in contest_list:
        valid_contest.add(i)

    url = "https://codeforces.com/api/user.status?handle="
    ret = {}

    for user in usernames:

        user = str(user)
        link = url + user
        js = get_json(link)

        if not js or "status" not in js or js["status"] != "OK":
            continue

        for submission in js["result"]:

            cid = submission["contestId"]
            idx = submission["problem"]["index"]

            if submission["verdict"] == "OK" and cid in valid_contest:
                if cid not in ret:
                    ret[cid] = {}
                    ret[cid]["user"] = {}
                if user not in ret[cid]["user"]:
                    ret[cid]["user"][user] = set()

                ret[cid]["user"][user].add(idx)

    for cid in ret:
        ret[cid]["name"] = contest_list[cid]

    for (cid, cdata) in ret.items():
        for (user, solve) in cdata["user"].items():
            ret[cid]['user'][user] = list(ret[cid]['user'][user])
            ret[cid]['user'][user] = sorted(ret[cid]['user'][user])

        for ppl in usernames:
            if ppl not in ret[cid]['user']:
                ret[cid]['user'][ppl] = []

    return ret

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
