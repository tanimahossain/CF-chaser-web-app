from operator import itemgetter

def makeContestDict(id, name):
    data = {}
    data['id'] = id
    data['name'] = name
    data['friend_solve'] = [0 for k in range(45)]
    data['my_solve'] = [0 for k in range(45)]
    data['lagging'] = 0
    data['advancing'] = 0
    return data

def makeData(contest_list, api_dict, username, friend_list):
    contest = []

    for contestId in contest_list:
        contestData = api_dict
        data = makeContestDict(contestId, contestData[contestId]['name'])

        solve_list = api_dict[contestId]['user'][username]
        for i in solve_list:
            x = (ord(i[0])-65)*2
            data['my_solve'][x]=1
            if len(i)>1:
                data['my_solve'][x+1]=1

        for i in friend_list:
            i = str(i)
            solve_list = api_dict[contestId]['user'][i]
            for j in solve_list:
                k = (ord(j[0])-65)*2
                data['friend_solve'][k] += 1
                if len(j) > 1:
                    data['friend_solve'][k + 1] = 1

        for i in range(40):
            if data['my_solve'][i]>0 and data['friend_solve'][i]==0:
                data['advancing'] += 1
            if data['my_solve'][i]==0 and data['friend_solve'][i]>0:
                data['lagging'] += 1
        contest.append(data)

    contest = sorted(contest, key=itemgetter('id'), reverse=True)
    return contest