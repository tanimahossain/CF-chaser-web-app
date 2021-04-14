from . import cfapi_handler
from .models import Friend

class DP:

    friend_profile=[]
    my_profile={}

    friend_data=[]       # for Friend List

    # data processing for friend_list page
    def friendListData(self):
        for i in self.friend_profile:
            self.friend_data.append(i)

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
            return [15, 222, 222, 0, 222, 222]
        elif rating<1900:
            return [0, 0, 255, 0, 0, 255]
        elif rating<2200:
            return [214, 56, 214, 214, 56, 214]
        elif rating<2400:
            return [255, 165, 0, 255, 165, 0]
        elif rating<3000:
            return [255, 0, 0, 255, 0, 0]
        else:
            return [0, 0, 0, 255, 0, 0]

    # processing profile data
    def getProfileData(self, username):
        profile = cfapi_handler.user_profile(username=username)

        profile['handle1'] = profile['handle'][0]
        profile['handle2'] = profile['handle'][1:]

        color = self.getColor(self, profile['cur_rating'])
        handle_color1 = color[0:3]
        handle_color2 = color[3:]
        cur_rating_color = color[3:]

        color = self.getColor(self, profile['max_rating'])
        max_rating_color = color[3:]

        profile['r1'] = handle_color1[0]
        profile['g1'] = handle_color1[1]
        profile['b1'] = handle_color1[2]

        profile['r2'] = handle_color2[0]
        profile['g2'] = handle_color2[1]
        profile['b2'] = handle_color2[2]

        profile['crr'] = cur_rating_color[0]
        profile['crg'] = cur_rating_color[1]
        profile['crb'] = cur_rating_color[2]

        profile['mrr'] = max_rating_color[0]
        profile['mrg'] = max_rating_color[1]
        profile['mrb'] = max_rating_color[2]

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
