import os

from pymongo import MongoClient

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
url = os.getenv('URL')
client = MongoClient('mongodb://{0}:27017'.format(url),
                     username=username,
                     password=password)


def insert_ad(ad):
    collection = client['bf-notifier']['ads']
    collection.replace_one({'Lägenhetsnummer': ad['Lägenhetsnummer'], 'AnnonsId': ad['AnnonsId']}, ad, upsert=True)


def retrieve(ad_filter):
    collection = client['bf-notifier']['ads']
    return collection.find(ad_filter)


def retrieve_all():
    return retrieve({})
