import sqlite3
from sqlite3 import Error
import os


def create_db(dbname="myappdb.db"):
    if not os.path.isfile(dbname):
        try:
            conn = sqlite3.connect(dbname, timeout=30)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
