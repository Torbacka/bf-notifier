import os

from pymongo import MongoClient

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

client = MongoClient('mongodb://mongodb:27017',
                     username=username,
                     password=password)


def insertAd(ad):
    collection = client['bfNotifier']['ads']
    collection.replace_one({'Lägenhetsnummer': ad['Lägenhetsnummer'], 'AnnonsId': ad['AnnonsId']}, ad, upsert=True)


def retrieveAll():
    collection = client['bfNotifier']['ads']
    return collection.find()

