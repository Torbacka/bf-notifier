from pymongo import MongoClient

client = MongoClient('mongodb://mongodb:27017',
                           username='root',
                           password='root')

def insertAd(ad):
    collection = client['bfNotifier']['ads']
    collection.insert_one(ad)


def retrieveAll():
    collection = client['bfNotifier']['ads']
    return collection.find()

def retrieveInterval(date1, date2):
    print("TODO")

    # Make some more retrieve
