from . import cfapi_handler, profileDataMaker
from .models import Friend

class profile:

    friend_profile=[]
    my_profile={}
    cur_user = ''

    def clearData(self):
        self.friend_data = []
        self.friend_profile = []
        self.my_profile = {}
        self.contest = []
        self.all_contest_id = []
        self.cur_user = ''

    # processing profile data
    def processProfileData(self, profile):
        profile = profileDataMaker.profileColoring(profile)
        return profile

    def addOneData(self, username):
        username = str(username)
        profile = cfapi_handler.user_profile([username])
        profile = profile[str(username)]
        return self.processProfileData(self, profile)

    def removeFriend(self, username):
        self.friend_profile = list(filter(lambda i: i['handle'] != username, self.friend_profile))

    def addFriend(self, username):
        data = self.addOneData(self, username)
        self.friend_profile.append(data)

    def addAllData(self, username):
        fr = Friend.objects.filter(friend_of__username=username)

        fr_list = []
        for i in fr:
            fr_list.append(str(i))
        if len(fr_list)==0:
            return

        data = cfapi_handler.user_profile(fr_list)
        for friend in fr_list:
            self.friend_profile.append(self.processProfileData(self, data[friend]))

    def getProfileData(self, username):
        username = str(username)
        self.my_profile = self.addOneData(self, username)
        self.addAllData(self, username)
