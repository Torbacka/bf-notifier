from pymongo import MongoClient

client = MongoClient('example.com',
                           username='user',
                           password='password',
                           authSource='the_database',
                           authMechanism='SCRAM-SHA-1')

def insertAd(ad):
    collection = client['bfNotifier']['ads']
    collection.insert_one(ad)


def retrieveAll():
    collection = client['bfNotifier']['ads']
    return collection.find()

def retrieveInterval(date1, date2):
    print("TODO")

    # Make some more retrieve
