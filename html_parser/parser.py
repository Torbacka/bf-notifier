from urllib.request import urlopen
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
    reponse = urlopen("https://bostad.stockholm.se"+url)
    html = reponse.read()
    soup = BeautifulSoup(html, 'html.parser')
    allCharacteristics = soup.find_all('div', class_="egenskap")
    ret = []
    for characteristics in allCharacteristics:
        n = characteristics.find('div', attrs={'class': 'n'})
        v = characteristics.find('div', attrs={'class': 'v'})
        ret.append(n.text.strip() + v.text.strip())

    statisticSoup = soup.find("div", {"id": "statistik-box"})
    queueTimes = statisticSoup.find_all('strong')
    i = 1
    for queueTimes in queueTimes:
        ret.append("Queue"+str(i)+":"+queueTimes.text)
        i+=1
    return ret
