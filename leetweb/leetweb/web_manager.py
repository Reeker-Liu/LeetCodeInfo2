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

def daily_notice():
    return


if __name__ == '__main__':
    print(1)
    print(get_en("we98"))
    print(get_en("huaji"))
    print(get_cn("dreamland"))
    print(get_cn("613"))