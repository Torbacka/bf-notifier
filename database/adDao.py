import pymysql
import pymysql.cursors


# insert an ad to the database
def insertAd(ad):
    database = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='',
        db='bfNotifier',
        charset='utf8',
        autocommit=True
    )

    cursor = database.cursor()
    sql = (
        'INSERT IGNORE INTO housingads(id,adress,type,publishDate, expireDate,price, rooms, livingSpace, webpage) VALUES' +
        ' (%s, %s, %s, %s,%s, %s, %s, %s,%s)')
    if "Lägenhetsnummer" in ad:
        id = ad['Lägenhetsnummer']
    else:
        id = ad['Gatuadress'] + ":" + ad['Antal rum']

    cursor.execute(sql, (
        id, ad['Gatuadress'], ad['Type'], ad['Annons publicerad'], ad['Anmälan senast'],
        ad['Hyra'], ad['Antal rum'], ad['Yta'], ad['Page']))

    # Update or insert queuetime depeding of value already exisit
    sql = 'SELECT * FROM queuetime WHERE housingAdID=%s'
    cursor.execute(sql, id)
    queue = ad['Queue']
    queue.sort()
    if cursor.rowcount > 0:
        i = 0
        for data in cursor:
            sql = 'UPDATE queuetime SET queueDate=%s WHERE id=%s'
            cursor.execute(sql,(queue[i],data[0]))
            i += 1
    else :
        sql = 'INSERT INTO queuetime (housingAdID, queueDate) VALUES (%s, %s)'
        for date in queue:
            cursor.execute(sql, (id, date))

    database.close()


def retrieveAll():
    ##Just for test will be removed later when Atila commits
    database = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='',
        db='bfNotifier',
        charset='utf8',
        autocommit=True
    )
    cursor = database.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM housingads'
    cursor.execute(sql)
    ads = []
    for data in cursor:
        ads.append(data)
    return ads

def retrieveInterval(date1, date2):
    print("TODO")

    # Make some more retrieve
