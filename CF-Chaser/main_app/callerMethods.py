from . import cfapi_handler, profileDataProcessor, contestDataProcessor
from .models import Friend

class massage:
    msg = ''

def checkUser(cfHandle):
    profile = cfapi_handler.user_profile([cfHandle])

    if cfHandle not in profile:
        return False
    else:
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