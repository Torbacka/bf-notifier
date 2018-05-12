from urllib2 import urlopen
from bs4 import BeautifulSoup
#parse bostad.stockholm.se/List page and returning a data structure containing all the links to ad page
def parseListPage(url):
    reponse = urlopen(url)
    html = reponse.read()
    soup = BeautifulSoup(html, 'html.parser')

    map = soup.find_all('a', class_="m-apartment-card")
    ret = []
    for x in map:
        ret.append(x['href'])
    return ret

# parse ad page and returning a data structure containing information about the ad
# queue time, type of ad, publish date, expire date, price, location, rent, number of rooms, living space
def parseAdPage(url):
    url ="https://bostad.stockholm.se"+url
    reponse = urlopen(url)
    html = reponse.read()
    soup = BeautifulSoup(html, 'html.parser')
    allCharacteristics = soup.find_all('div', class_="egenskap")
    ret = dict()
    ret['Page'] = url
    for characteristics in allCharacteristics:
        n = characteristics.find('div', attrs={'class': 'n'})
        v = characteristics.find('div', attrs={'class': 'v'})
        if(n != None):
            key = n.text.strip()[:-1]
            ret[key] = v.text.strip()

    statisticSoup = soup.find("div", {"id": "statistik-box"})
    queueTimes = statisticSoup.find_all('strong')

    queue = []
    for queueTimes in queueTimes:
        queue.append(queueTimes.text)
    ret["Queue"] = queue
    type = soup.find("span", attrs={'class': 'm-tag'})
    if type != None:
        ret['Type'] = type.text
    else:
        ret['Type'] = ""
    return ret
