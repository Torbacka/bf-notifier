from flask import Flask, jsonify
from werkzeug.contrib.cache import SimpleCache
from database import adDao
from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/v1/user/<string:user>', methods=['GET'])
def getAllAds(user):
    return jsonify('test')

#TODO post method to add one user


#TODO patch method to update/modify one user

if __name__ == '__main__':
    print("hej")