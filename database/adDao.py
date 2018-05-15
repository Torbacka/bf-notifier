from pymongo import MongoClient

client = MongoClient('mongodb://mongodb:27017',
                     username='root',
                     password='root')


def insertAd(ad):
    collection = client['bfNotifier']['ads']
    collection.replace_one({'Lägenhetsnummer': ad['Lägenhetsnummer'], 'AnnonsId': ad['AnnonsId']}, ad, upsert=True)


def retrieveAll():
    collection = client['bfNotifier']['ads']
    return collection.find()

