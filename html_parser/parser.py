import json
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup


# parse bostad.stockholm.se/List page and returning a data structure containing all the links to ad page
def parseListPage():
    response = urlopen("https://bostad.stockholm.se/Lista/AllaAnnonser")
    data = response.read()
    jsonData = json.loads(data)
    return jsonData


# parse ad page and returning a data structure containing information about the ad
# queue time, type of ad, publish date, expire date, price, location, rent, number of rooms, living space
def parseAdPage(ret, url):
    if bool(ret):
        ret = updateJson(ret)
    url = "https://bostad.stockholm.se" + url
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    allCharacteristics = soup.find_all('div', class_="egenskap")
    ret['Page'] = url
    for characteristics in allCharacteristics:
        n = characteristics.find('div', attrs={'class': 'n'})
        v = characteristics.find('div', attrs={'class': 'v'})
        if n is not None:
            key = fixKey(n)
            ret[key] = parseValue(key, v.text.strip())

    statistic_soup = soup.find("div", {"id": "statistik-box"})
    queue_times = []
    if statistic_soup is not None:
        queue_times = statistic_soup.find_all('strong')

    queue = []
    for queueTime in queue_times:
        queue.append(datetime.strptime(queueTime.text, '%Y-%m-%d'))
    ret["Queue"] = queue
    adType = soup.find("span", attrs={'class': 'm-tag'})
    if adType is not None:
        ret['Type'] = adType.text
    else:
        ret['Type'] = ""
    return ret


def updateJson(json):
    json['AnnonseradTill'] = datetime.strptime(json['AnnonseradTill'], '%Y-%m-%d')
    json['AnnonseradFran'] = datetime.strptime(json['AnnonseradFran'], '%Y-%m-%d')
    return json


def parseValue(key, value):
    if key == 'AnmälanSenast' or key == 'AnnonsPublicerad' or key == 'Inflyttning':
        return datetime.strptime(value, '%Y-%m-%d')
    else:
        return value


def fixKey(key):
    return key.text.strip()[:-1].title().replace(" ", "")
