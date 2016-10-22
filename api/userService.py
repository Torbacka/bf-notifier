from flask import Flask, jsonify
from werkzeug.contrib.cache import SimpleCache
from database import adDao
from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/v1/user/<string:user>', methods=['GET'])
def getAllAds(user):
    return jsonify('test')

#TODO post method to add one user
@user.route('/v1/user/', methods=['POST'])
def addUser():
    return jsonify('post user')

#TODO patch method to update/modify one user
@user.route('/v1/user/', methods=['PATCH'])
def updateUser():
    return jsonify('patch user')

if __name__ == '__main__':
    print("hej")