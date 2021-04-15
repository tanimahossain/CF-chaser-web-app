from . import cfapi_handler, profileDataProcessor, contestDataProcessor
from .models import Friend

def checkUser(cfHandle):
    profile = cfapi_handler.user_profile([cfHandle])

    if cfHandle not in profile:
        return False
    else:
        return True

def checkDataUpdate(cfHandle):
    if 'handle' not in profileDataProcessor.profile.my_profile:
        profileDataProcessor.profile.getProfileData(profileDataProcessor.profile, cfHandle)
        contestDataProcessor.contest.addAllContestData(contestDataProcessor.contest, cfHandle)

def clearData():
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

def addFriend(username):
    if len(profileDataProcessor.profile.friend_profile) == 20:
        return 1
    if not checkUser(username):
        return 2

    profileDataProcessor.profile.addFriend(profileDataProcessor.profile, username)
    contestDataProcessor.contest.addFriend(contestDataProcessor.contest, username)
    return 3

def removeFriend(username):
    fr = Friend.objects.filter(friend_of__username=username)

    if username in fr:
        profileDataProcessor.profile.removeFriend(profileDataProcessor.profile, username)
        contestDataProcessor.contest.removeFriend(contestDataProcessor.contest, username)
        return True
    else:
        return False