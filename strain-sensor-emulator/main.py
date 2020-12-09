import mysql.connector
from mysql.connector import errorcode
import sys


def db_connect():
    config = {
        'user': 'isac',
        'password': 'mysqlisac',
        'host': '192.168.1.10',
        'database': 'isac'
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


def insert(cnx):
    insert_query = ("INSERT INTO Strain (tag, name, data) VALUES (%(tag)s, %(name)s, %(data)s)")

    tag = 'strain-02'
    name = 'strain-02'
    data = '15.4'
    sensor_data = {
        'tag': tag,
        'name': name,
        'data': data
    }

    cur = cnx.cursor()
    try:
        cur.execute(insert_query, sensor_data)
        print("inserted successfully")
    except:
        print("not inserted")
    cnx.commit()


def main():
    cnx = db_connect()
    insert(cnx)
    db_close(cnx)


if __name__ == '__main__':
    main()