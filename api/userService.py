from flask import Flask, jsonify
from database import userDao
from flask import request
from flask import Blueprint

user = Blueprint('user', __name__)


@user.route('/v1/user/<string:user>', methods=['GET'])
def getAllAds(user):
    return jsonify('test')


@user.route('/v1/user', methods=['POST'])
def addUser():
    data = request.get_json()
    if ('name' in data):
        userDao.addUser(data['name'], data['maxRent'], data['rooms'], data['apartmentType'], data['distance'])
        print(data)
        return jsonify('User ' + data['name'] + ' was sucessfully added')
    else:
        return jsonify('Paramenter name is missing')


# TODO patch method to update/modify one user
@user.route('/v1/user/', methods=['PATCH'])
def updateUser():
    return jsonify('patch user')


if __name__ == '__main__':
    print("hej")
