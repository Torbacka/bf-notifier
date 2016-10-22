#!flask/bin/python
from flask import Flask, jsonify
from werkzeug.contrib.cache import SimpleCache
from database import adDao
from flask import Blueprint

cache = SimpleCache()

ads = Blueprint('ads', __name__)

#Hämtar alla ads från databasen och skickar tillbaka dessa i json format
@ads.route('/v1/ads/', methods=['GET'])
def getAllAds():
    return jsonify(getAdsFromCacheOrDB())

#Filtrerar alla ads  med hjälp av ett datum. TODO kanske byta ut path parameters till query parameters
@ads.route('/v1/ads/date/<string:date>')
def getAdsFilterOnDate(date):
    ads = getAdsFromCacheOrDB()
    ads = filter(lambda x: x.expireDate < date, ads)
    return jsonify(ads)

#TODO Göra lite andra api metoder



#Hämtar ads from cache eller databasen
def getAdsFromCacheOrDB():
    ads = cache.get('all-ads')
    if ads is None:
        ads = adDao.retrieveAll()
        cache.set('all-ads', ads, timeout=12 * 60 * 60)
    return ads


if __name__ == '__main__':
    print("running")
