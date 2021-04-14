from . import cfapi_handler
from .models import Friend

class DP:

    friend_profile=[]
    my_profile={}

    friend_data=[]       # for Friend List

    # data processing for friend_list page
    def friendListData(self):
        for i in self.friend_profile:
            self.friend_data.append({
                'handle' : i['handle'],
                'cur_rating' : i['cur_rating'],
                'max_rating' : i['max_rating']
            })

    # to get the data for profile page
    def profileData(self):
        return self.my_profile


    # color determination
    def getColor(self, rating):
        if rating<1200:
            return [128, 128, 128, 128, 128, 128]
        elif rating<1400:
            return [12, 115, 12, 12, 115, 12]
        elif rating<1600:
            return [0, 255, 255, 0, 255, 255]
        elif rating<1900:
            return [0, 0, 255, 0, 0, 255]
        elif rating<2200:
            return [238, 130, 238, 238, 130, 238]
        elif rating<2400:
            return [255, 165, 0, 255, 165, 0]
        elif rating<3000:
            return [255, 0, 0, 255, 0, 0]
        else:
            return [0, 0, 0, 255, 0, 0]

    # processing profile data
    def getProfileData(self, username):
        profile = cfapi_handler.user_profile(username=username)

        profile['handle_1st'] = profile['handle'][0]
        profile['handle_last'] = profile['handle'][1:]

        color = self.getColor(self, profile['cur_rating'])
        profile['handle_color1'] = color[0:3]
        profile['handle_color2'] = color[3:]
        profile['cur_rating_color'] = color[3:]

        color = self.getColor(self, profile['max_rating'])
        profile['max_rating_color'] = color[3:]

        return profile

    # after adding a friend update data
    def addInfo(self, username):
        username = str(username)
        info = self.getProfileData(self, username)
        self.friend_profile.append(info)

    def clearData(self):
        self.friend_data = []
        self.friend_profile = []
        self.my_profile = {}

    # after log in update all friend data
    def addAll(self, username):
        username = str(username)
        fr = Friend.objects.filter(friend_of__username=username)

        self.my_profile = self.getProfileData(self, username)
        for i in fr:
            self.addInfo(self, username=i)

        self.friendListData(self)
