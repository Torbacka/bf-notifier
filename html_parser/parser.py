import json
from urllib2 import urlopen
from bs4 import BeautifulSoup


# parse bostad.stockholm.se/List page and returning a data structure containing all the links to ad page
def parseListPage():
    response = urlopen("https://bostad.stockholm.se/Lista/AllaAnnonser")
    data = response.read()
    jsonData = json.loads(data)
    return jsonData


# parse ad page and returning a data structure containing information about the ad
# queue time, type of ad, publish date, expire date, price, location, rent, number of rooms, living space
def parseAdPage(url):
    url = "https://bostad.stockholm.se" + url
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    allCharacteristics = soup.find_all('div', class_="egenskap")
    ret = dict()
    ret['Page'] = url
    for characteristics in allCharacteristics:
        n = characteristics.find('div', attrs={'class': 'n'})
        v = characteristics.find('div', attrs={'class': 'v'})
        if n is not None:
            key = n.text.strip()[:-1]
            ret[key] = v.text.strip()

    statisticSoup = soup.find("div", {"id": "statistik-box"})
    queueTimes = statisticSoup.find_all('strong')

    queue = []
    for queueTimes in queueTimes:
        queue.append(queueTimes.text)
    ret["Queue"] = queue
    type = soup.find("span", attrs={'class': 'm-tag'})
    if type is not None:
        ret['Type'] = type.text
    else:
        ret['Type'] = ""
    return ret
