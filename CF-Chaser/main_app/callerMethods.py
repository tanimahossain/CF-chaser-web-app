from . import cfapi_handler, profileDataProcessor, contestDataProcessor
from .models import Friend

class massage:
    msg = ''

def checkUser(cfHandle):
    profile = cfapi_handler.user_profile([cfHandle])

    if cfHandle not in profile:
        return False
    elif 'handle' not in profile[cfHandle]:
        return False
    else:
        print(profile)
        return True

def checkDataUpdate(cfHandle):
    if 'handle' not in profileDataProcessor.profile.my_profile:
        profileDataProcessor.profile.cur_user = cfHandle
        contestDataProcessor.contest.cur_user = cfHandle
        profileDataProcessor.profile.getProfileData(profileDataProcessor.profile, cfHandle)
        contestDataProcessor.contest.addAllContestData(contestDataProcessor.contest, cfHandle)

def clearData():
    massage.msg = ''
    profileDataProcessor.profile.clearData(profileDataProcessor.profile)
    contestDataProcessor.contest.clearData(contestDataProcessor.contest)

def getProfileData(username):
    checkDataUpdate(username)
    return profileDataProcessor.profile.my_profile

def getFriendListData(username):
    checkDataUpdate(username)
    return profileDataProcessor.profile.friend_profile

def getChessByContestData(username):
    checkDataUpdate(username)
    return contestDataProcessor.contest.chaseByContest(contestDataProcessor.contest, username)

def addFriend(username, me):
    print('username = ', username)
    if len(profileDataProcessor.profile.friend_profile) == 20:
        return 1
    if not checkUser(username):
        return 2

    fr = Friend.objects.filter(friend_of__username=me.username)
    fr = [str(i) for i in fr]
    if username in fr:
        return 3

    profileDataProcessor.profile.addFriend(profileDataProcessor.profile, username)
    contestDataProcessor.contest.addFriend(contestDataProcessor.contest, username)

    friend = Friend()
    friend.cfHandle = username
    friend.friend_of = me
    friend.save()
    return 4

def removeFriend(username, me):
    fr = Friend.objects.filter(friend_of__username=me.username)
    fr = [str(i) for i in fr]

    if username in fr:
        profileDataProcessor.profile.removeFriend(profileDataProcessor.profile, username)
        contestDataProcessor.contest.removeFriend(contestDataProcessor.contest, username)

        friend = Friend.objects.get(cfHandle=username)
        friend.delete()
        return True
    else:
        return False

def getContestDetails(username, id):
    checkDataUpdate(username)
    detail = contestDataProcessor.contest.api_dict[id]['user']

    ret = []
    handle_list = [profileDataProcessor.profile.my_profile]

    for i in profileDataProcessor.profile.friend_profile:
        handle_list.append(i)

    for i in handle_list:
        user = i['handle']

        solve = detail[user]
        solve = sorted(solve)

        solve_list=''
        cnt=0

        for j in solve:
            if cnt>0:
                solve_list += ', '
            solve_list += j
            cnt += 1

        if len(solve_list)==0:
            solve_list += 'None'
        i['solve_list'] = solve_list
        ret.append(i)
    ret['contest_name'] = contestDataProcessor.contest.api_dict[id]['name']

    return ret