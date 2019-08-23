import json
import locale
import re
from datetime import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup

locale.setlocale(locale.LC_TIME, "sv_SE.UTF-8")


# parse bostad.stockholm.se/List page and returning a data structure containing all the links to ad page
def parse_list_page():
    response = urlopen("https://bostad.stockholm.se/Lista/AllaAnnonser")
    data = response.read()
    json_data = json.loads(data)
    return json_data


# parse ad page and returning a data structure containing information about the ad
# queue time, type of ad, publish date, expire date, price, location, rent, number of rooms, living space
def parse_ad_page(ad_data, url, html):
    if bool(ad_data):
        ad_data = convert_to_datetime(ad_data)
    ad_data['url'] = url
    soup = BeautifulSoup(html, 'html.parser')
    # Update the dict with all the data from the class tag "egenskap"
    ad_data.update(extract_all_characteristics(soup))
    # Update the queue information if it exist
    ad_data["queue"] = extract_queue_data(soup.find("div", {"id": "statistik-box"}))
    extract_information_text(ad_data, soup)
    ad_data['apartmentInfo'] = [info.text for info in soup.find("div", {'class': 'inner colBox'}).findAll('li')]
    # Update the ad type if it exist
    ad_data['type'] = extract_ad_type(soup.find("span", attrs={'class': 'm-tag'}))
    return ad_data


def extract_information_text(ad_data, soup):
    information_text = soup.find("strong", attrs={'class': 'error'})
    if information_text is not None:
        info = information_text.text
        if "Kötid:" in info:
            info_split = info.split("Kötid:")
            ad_data["winningTime"] = datetime.strptime(info_split[1].strip(), '%b %Y')
        ad_data['information'] = info.strip()


def extract_ad_type(ad_type):
    if ad_type is not None:
        return ad_type.text
    else:
        return ""


def extract_all_characteristics(soup):
    ad_data = dict()
    all_characteristics = soup.find_all('div', class_="egenskap")
    for characteristics in all_characteristics:
        n = characteristics.find('div', attrs={'class': 'n'})
        v = characteristics.find('div', attrs={'class': 'v'})
        if n is not None:
            key = parse_key(fix_key(n))
            ad_data[key] = parse_value(key, v.text.strip())
    return ad_data


def extract_queue_data(statistic_soup):
    queue_times = []
    if statistic_soup is not None:
        queue_times = statistic_soup.find_all('strong')
    queue = []
    for queueTime in queue_times:
        queue.append(datetime.strptime(queueTime.text, '%Y-%m-%d'))
    return queue


def convert_to_datetime(json_dict):
    json_dict['advertisedTo'] = datetime.strptime(json_dict['advertisedTo'], '%Y-%m-%d')
    json_dict['advertisedFrom'] = datetime.strptime(json_dict['advertisedFrom'], '%Y-%m-%d')
    return json_dict


def parse_value(key, value):
    if key == 'registerLast' or key == 'published' or key == 'occupancy':
        return datetime.strptime(value, '%Y-%m-%d')
    else:
        numbers = re.findall(r"[-+]?\d+", value)
        if len(numbers) and (key != 'address' or key != 'apartmentNumber'):
            return int(numbers[0])
        return value


def parse_key(key):
    translation = {
        'Lägenhetsnummer': 'apartmentNumber',
        'Inflyttning': 'occupancy',
        'Ritning': 'plan',
        'Våning': 'floor',
        'Hyra': 'rent',
        'Yta': 'area',
        'Gatuadress': 'address',
        'AnnonsPublicerad': 'published',
        'AnmälanSenast': 'registerLast',
        'AntalRum': 'rooms'
    }
    if key in translation:
        return translation[key]
    else:
        return key


def fix_key(key):
    return key.text.strip()[:-1].title().replace(" ", "")
