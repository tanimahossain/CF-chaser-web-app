from . import cfapi_handler, contestDataMaker
from .models import Friend

class contest:
    api_dict = {}
    contest_list = set()
    contest = []
    ok = False

    def clearData(self):
        self.api_dict = {}
        self.contest_list = set()
        self.contest = []

    def chaseByContest(self, username):
        if not self.ok:
            fr = Friend.objects.filter(friend_of__username=username)
            self.contest = contestDataMaker.makeData(self.contest_list, self.api_dict, username, fr)
            self.ok = True

        data = []
        for i in self.contest:
            x = {}
            x['id'] = i['id']
            x['name'] = i['name']
            x['lagging'] = i['lagging']
            x['advancing'] = i['advancing']
            data.append(x)
        return data

    def makeContestList(self):
        self.ok = False
        self.contest_list = set()

        for i, j in self.api_dict.items():
            cnt=0
            for name, k in self.api_dict[i]['user'].items():
                cnt += len(k)

            if cnt>0:
                self.contest_list.add(i)

    def removeFriend(self, username):
        for i, j in self.api_dict.items():
            self.api_dict[i]['user'][username]=[]
        self.makeContestList(self)

    def addFriend(self, username):
        new_frnd = cfapi_handler.contest_participation([username])
        self.api_dict[username] = new_frnd[username]
        self.makeContestList(self)

    def addAllContestData(self, username):
        username = str(username)
        l = [username]

        fr = Friend.objects.filter(friend_of__username=username)
        for i in fr:
            l.append(str(i))

        self.api_dict = cfapi_handler.contest_participation(l)
        self.makeContestList(self)