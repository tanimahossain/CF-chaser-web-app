from . import cfapi_handler, profileDataMaker
from .models import Friend

class profile:

    friend_profile=[]
    my_profile={}

    def clearData(self):
        self.friend_data = []
        self.friend_profile = []
        self.my_profile = {}
        self.contest = []
        self.all_contest_id = []

    # processing profile data
    def processProfileData(self, profile):
        profile = profileDataMaker.profileColoring(profile)
        return profile

    def addOneData(self, username):
        username = str(username)
        profile = cfapi_handler.user_profile([username])

        profile = profile[username]
        return self.processProfileData(self, profile)

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



    #
    # def checkSortedContestList(self):
    #     if not self.is_sorted:
    #         self.contest = sorted(self.contest, key=itemgetter('id'), reverse=True)
    #         self.all_contest_id = sorted(self.all_contest_id, reverse=True)
    #         self.is_sorted = True
    #
    # # data for chase by contest page
    # def chaseByContestData(self):
    #     data = []
    #     for i in self.contest:
    #         x = {}
    #         x['id'] = i['id']
    #         x['name'] = i['name']
    #         x['lagging'] = i['lagging']
    #         x['advancing'] = i['advancing']
    #         data.append(x)
    #
    #     return  data
    #
    # # to get the data for profile page
    # def profileData(self):
    #     return self.my_profile
    #
    #

    #
    # def makeContestDict(self, i):
    #     data = {}
    #     data['id'] = i['id']
    #     data['name'] = i['name']
    #     data['friend_solve'] = [0 for k in range(45)]
    #     data['my_solve'] = [0 for k in range(45)]
    #     data['my_solve_list'] = ""
    #     data['participants'] = []
    #     data['lagging'] = 0
    #     data['advancing'] = 0
    #     data['total_ac'] = 0
    #     return data
    #
    # def updateNewContestData(self, data):
    #     solve_list = cfapi_handler.contest_solve(self.my_profile['handle'], data['id'])
    #     data['total_ac'] += len(solve_list)
    #     loop_count = 0
    #     for i in solve_list:
    #         x = (ord(i[0])-65)*2
    #         data['my_solve'][x]=1
    #         if len(i)>1:
    #             data['my_solve'][x+1]=1
    #         if loop_count>0:
    #             data['my_solve_list'] += ", "
    #         data['my_solve_list'] += i
    #         loop_count += 1
    #
    #     for i in self.friend_profile:
    #         x = i
    #         x['solve_list'] = ""
    #         solve_list = cfapi_handler.contest_solve(x['handle'], data['id'])
    #         data['total_ac'] += len(solve_list)
    #         loop_count = 0
    #         for i in solve_list:
    #             k = (ord(i[0])-65)*2
    #             data['friend_solve'][k] += 1
    #             if len(i) > 1:
    #                 data['friend_solve'][k + 1] = 1
    #             if loop_count>0:
    #                 x['solve_list'] += ", "
    #             x['solve_list'] += i
    #
    #         data['participants'].append(x)
    #
    #     for i in range(40):
    #         if data['my_solve'][i]>0 and data['friend_solve'][i]==0:
    #             data['advancing'] += 1
    #         if data['my_solve'][i]==0 and data['friend_solve'][i]>0:
    #             data['lagging'] += 1
    #
    #     return data
    #
    #
    # # process data for all contests and friends
    # def makeContestData(self, contest_list):
    #     for i in contest_list:
    #         if i['id'] in self.all_contest_id:
    #             self.contest = list(filter(lambda j: j['id'] != i['id'], self.contest))
    #         data = self.makeContestDict(self, i)
    #         data = self.updateNewContestData(self, data)
    #         if i['id'] not in self.all_contest_id:
    #             self.all_contest_id.append(i['id'])
    #         self.contest.append(data)
    #         self.is_sorted = False
    #
    #
    # # after adding a friend and update data
    # def addFriend(self, username):
    #     username = str(username)
    #     info = self.getProfileData(self, username)
    #     self.friend_profile.append(info)
    #
    #     contest_list = cfapi_handler.contest_participation(username)
    #     self.makeContestData(self, contest_list)
    #
    # # after log in update all friend data
    # def addAll(self, username):
    #     username = str(username)
    #     fr = Friend.objects.filter(friend_of__username=username)
    #
    #     # self.my_profile = self.getProfileData(self, username)
    #     # contest_list = cfapi_handler.contest_participation(username)
    #     # self.makeContestData(self, contest_list)
    #     for i in fr:
    #         self.addFriend(self, username=i)
    #
    #     self.friendListData(self)


