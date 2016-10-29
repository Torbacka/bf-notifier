import pymysql
import pymysql.cursors


def addUser(name, maxRent, rooms, apartmentType, distance):
    database = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='',
        db='bfNotifier',
        charset='utf8',
        autocommit=True
    )

    cursor = database.cursor()
    sql = ('INSERT IGNORE INTO user(name,maxRent, rooms, apartmentType, distance) VALUES (%s, %s, %s, %s,%s)')
    cursor.execute(sql, (name, maxRent, rooms, apartmentType, distance))
    database.close()


def getUser(name):
    database = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='',
        db='bfNotifier',
        charset='utf8',
        autocommit=True
    )
    cursor = database.cursor(pymysql.cursors.DictCursor)
    sql = ('SELECT * FROM user WHERE name = %S')
    cursor.execute(sql, name)
    return cursor.fetchone()
