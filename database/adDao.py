import pymysql
import pymysql.cursors
import base64

# insert an ad to the database


def insertAd(ad):
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='',
        db='bfNotifier',
        autocommit=True
    )

    cur = conn.cursor()
    sql = ('INSERT INTO housingads(id,adress,type,publishDate, expireDate,price, rooms, livingSpace, webpage) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s)')
    if "Lägenhetsnummer" in ad:
        id = ad['Lägenhetsnummer']+"ö"
    else:
        data = ad['Gatuadress'] + ":" + ad['Antal rum']

        id = base64.standard_b64encode(bytes(data,'UTF-8'))

    cur.execute(sql,(
        id, ad['Gatuadress'] ,"Test" , ad['Annons publicerad'] , ad[
            'Anmälan senast'], ad['Hyra'] , ad['Antal rum'],ad['Yta'] ,"test"))

    #id = conn.insert_id()
    cur = conn.cursor()
    sql = ('INSERT INTO queuetime(housingAdID, queueDate) VALUES (%s, %s)')
    queue = ad['queue']
    print(id)
    for date in queue:
        cur.execute(sql, (id, date))

    conn.close()


def retrieveAll():
    print("TODO")


def retrieveInterval(date1, date2):
    print("TODO")

    # Make some more retrieve
