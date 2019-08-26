import os

from pymongo import MongoClient

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
url = os.getenv('URL')
client = MongoClient(f"mongodb://{username}:{password}@hack-for-sweden-shard-00-00-7vayj.mongodb.net:27017,hack-for-sweden-shard-00-01-7vayj.mongodb.net:27017,"
                     "hack-for-sweden-shard-00-02-7vayj.mongodb.net:27017/test?ssl=true&replicaSet=hack-for-sweden-shard-0&authSource=admin&retryWrites=true")


def insert_ad(ad):
    collection = client['bf-notifier']['ads']
    collection.replace_one({'apartmentNumber': ad.get('apartmentNumber'), 'adId': ad['adId']}, ad, upsert=True)


def retrieve(ad_filter):
    collection = client['bf-notifier']['ads']
    return collection.find(ad_filter)


def retrieve_all():
    return retrieve({})
