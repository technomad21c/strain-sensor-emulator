import mysql.connector
from mysql.connector import errorcode
import sys
import time
import signal

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


def insert(cnx, data):
    insert_query = ("INSERT INTO Strain (tag, name, data) VALUES (%(tag)s, %(name)s, %(data)s)")

    tag = 'strain-01'
    name = 'strain-01'
    sensor_data = {
        'tag': tag,
        'name': name,
        'data': data
    }

    cur = cnx.cursor()
    try:
        cur.execute(insert_query, sensor_data)
    except:
        print("not inserted")
    cnx.commit()

def signal_handler(signal, frame):
    print('stopped with ctrl-c')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    cnx = db_connect()
    with open('strain-sensor-data.csv', 'r') as f:
        data = [line.strip() for line in f.readlines()]

    while True:
        for d in data:
            print(d)
            # insert(cnx, d)
            time.sleep(1)

    db_close(cnx)

if __name__ == '__main__':
    main()