import mysql.connector
from mysql.connector import errorcode
import sys
import time


def db_connect():
    config = {
        'user': 'user',
        'password': 'password',
        'host': '192.168.1.2',
        'database': 'db'
    }

    cnx = None

    try:
        cnx = mysql.connector.connect(**config)
        print("successfully got connection")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("invalid user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("invalid database")
        else:
            print("exception occurs")

    return cnx


def db_close(cnx):
    cnx.cursor().close()
    cnx.close()


def insert(cnx, data):
    insert_query = ("INSERT INTO Strain (tag, name, data) VALUES (%(tag)s, %(name)s, %(data)s)")

    tag = 'strain-03'
    name = 'strain-03'
    sensor_data = {
        'tag': tag,
        'name': name,
        'data': data
    }

    cur = cnx.cursor()
    try:
        cur.execute(insert_query, sensor_data)
        print("successfully inserted to database: ", data)
    except:
        print("not inserted")
    cnx.commit()


def main():
    cnx = db_connect()

    with open('strain-sensor-data.csv', 'r') as f:
        data = f.readline().strip()
        while data != '':
            insert(cnx, data)
            time.sleep(1)
            data = f.readline().strip()

    db_close(cnx)

if __name__ == '__main__':
    main()