from django.http import HttpResponse
from django.shortcuts import render
from users.models import User
import re
import requests
import json


def get_cn(id):
    payload_data = {
        'operationName': "userPublicProfile",
        'query': 'query userPublicProfile($userSlug: String!) {  userProfilePublicProfile(userSlug: $userSlug) {    username    haveFollowed    siteRanking    profile {      userSlug      realName      aboutMe      userAvatar      location      gender      websites      skillTags      contestCount      asciiCode      ranking {        rating        ranking        currentLocalRanking        currentGlobalRanking        currentRating        ratingProgress        totalLocalUsers        totalGlobalUsers        __typename      }      skillSet {        langLevels {          langName          langVerboseName          level          __typename        }        topics {          slug          name          translatedName          __typename        }        topicAreaScores {          score          topicArea {            name            slug            __typename          }          __typename        }        __typename      }      socialAccounts {        provider        profileUrl        __typename      }      __typename    }    educationRecordList {      unverifiedOrganizationName      __typename    }    occupationRecordList {      unverifiedOrganizationName      jobTitle      __typename    }    submissionProgress {      totalSubmissions      waSubmissions      acSubmissions      reSubmissions      otherSubmissions      acTotal      questionTotal      __typename    }    __typename  }}',
        'variables': {'userSlug': id}
    }

    payload_header = {
        'Host': 'leetcode-cn.com',
        'Content-Type': 'application/json'
    }

    response = requests.post('https://leetcode-cn.com/graphql', data=json.dumps(payload_data), headers=payload_header)
    items = re.findall(r'acTotal.*?,', response.text, re.S)
    if len(items) == 0:
        return None
    
    ac = items[0][9:-1]
    # print(ac)
    return int(ac)


def get_en(id):
    response = requests.get('https://leetcode.com/' + id)
    items = re.findall(r'progress-bar-success.*?</span>', response.text, re.S)
    if len(items) == 0:
        return None

    items = [i[22:-8].strip() for i in items]
    # print(items)

    temp = []
    for item in items:
        if item.count("/") > 0:
            temp.append(item)
    items = temp
    # print(items)

    items = items[-2:]

    ac, aq = str.split(items[0], '/')
    # acsub, allsub = str.split(items[1], '/')
    
    return int(ac)


def get_ac(id, version):
    if version == 0:
        return get_en(id)
    else:
        return get_cn(id)


def main(request):
    context_dict = {}

    users_set = User.objects.all().filter(latest__gt=0).order_by('-latest')
    users = [[i.name, i.yesterday, i.today, i.latest, i.id] for i in users_set]

    leaderboard_list = []
    for i in range(len(users)):
        leaderboard_list.append([i+1, users[i][0], users[i][3]])
    context_dict["leaderboard_list"] = leaderboard_list

    func = lambda x : x[1]

    yesterday_list = [[i[0], i[2]-i[1]] for i in users if i[2]-i[1] != 0 ]
    yesterday_list.sort(key=func, reverse=True)
    if len(yesterday_list) == 0:
        yesterday_list.append(['-', 0])
    context_dict["yesterday_list"] = yesterday_list

    today_list = [[i[0], i[3]-i[2]] for i in users if i[3]-i[2] != 0 ]
    today_list.sort(key=func, reverse=True)
    if len(today_list) == 0:
        today_list.append(['-', 0])
    context_dict["today_list"] = today_list

    return render(request, 'index.html', context_dict)


# 接收POST请求数据
def register(request):
    name = request.POST['nickname']
    id = request.POST['leetcode_id']
    email = request.POST['email']
    version = request.POST['leetcode_version']
    # if version == "EN":
    #     version = 0
    # else:
    #     version = 1

    result = 'Failed, ID already exists'
    try:
        User.objects.get(id=id)
    except User.DoesNotExist:
        obj = User.objects.create(name=name, id=id, email=email, version=version)
        result = 'Complete' + str(obj)
    result_dict = {'result': result}
    return render(request, "result.html", result_dict)


def update(request):
    ac_set = []
    for user in User.objects.all():
        ac = None
        try:
            ac = get_ac(user.id, user.version)
        except:
            pass
        if ac == None:
            ac = 0
        ac_set.append([user.name, ac])
        user.latest = ac
        user.save()
    return HttpResponse("update done.\n" + str(ac_set))


def update_daily(request):
    for user in User.objects.all():
        user.yesterday = user.today
        user.today = user.latest
        user.save()
    return HttpResponse("update daily done.")


def clear_all(request):
    User.objects.all().delete()
    return HttpResponse("clear all done.")

def clear_invalid(request):
    User.objects.all().filter(latest=0).delete()
    return HttpResponse("clear invalid done.")
