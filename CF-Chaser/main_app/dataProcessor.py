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

    # after adding a friend update data
    def addInfo(self, username):
        username = str(username)
        info = cfapi_handler.user_profile(username=username)
        self.friend_profile.append(info)

    # after log in update all friend data
    def addAll(self, username):
        username = str(username)
        fr = Friend.objects.filter(friend_of__username=username)

        self.my_profile = cfapi_handler.user_profile(username=username)
        for i in fr:
            self.addInfo(username=i)

        self.friendListData()
