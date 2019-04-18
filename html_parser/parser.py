import json
from datetime import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup


# parse bostad.stockholm.se/List page and returning a data structure containing all the links to ad page
def parse_list_page():
    response = urlopen("https://bostad.stockholm.se/Lista/AllaAnnonser")
    data = response.read()
    json_data = json.loads(data)
    return json_data


# parse ad page and returning a data structure containing information about the ad
# queue time, type of ad, publish date, expire date, price, location, rent, number of rooms, living space
def parse_ad_page(ret, url):
    if bool(ret):
        ret = update_json(ret)
    url = "https://bostad.stockholm.se" + url
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    all_characteristics = soup.find_all('div', class_="egenskap")
    ret['Page'] = url
    for characteristics in all_characteristics:
        n = characteristics.find('div', attrs={'class': 'n'})
        v = characteristics.find('div', attrs={'class': 'v'})
        if n is not None:
            key = fix_key(n)
            ret[key] = parse_value(key, v.text.strip())

    statistic_soup = soup.find("div", {"id": "statistik-box"})
    queue_times = []
    if statistic_soup is not None:
        queue_times = statistic_soup.find_all('strong')

    queue = []
    for queueTime in queue_times:
        queue.append(datetime.strptime(queueTime.text, '%Y-%m-%d'))
    ret["Queue"] = queue
    ad_type = soup.find("span", attrs={'class': 'm-tag'})
    if ad_type is not None:
        ret['Type'] = ad_type.text
    else:
        ret['Type'] = ""
    return ret


def update_json(json_dict):
    json_dict['AnnonseradTill'] = datetime.strptime(json_dict['AnnonseradTill'], '%Y-%m-%d')
    json_dict['AnnonseradFran'] = datetime.strptime(json_dict['AnnonseradFran'], '%Y-%m-%d')
    return json_dict


def parse_value(key, value):
    if key == 'AnmälanSenast' or key == 'AnnonsPublicerad' or key == 'Inflyttning':
        return datetime.strptime(value, '%Y-%m-%d')
    else:
        return value


def fix_key(key):
    return key.text.strip()[:-1].title().replace(" ", "")
