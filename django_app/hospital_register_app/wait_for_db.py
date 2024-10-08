import os
import time
import MySQLdb

def wait_for_db():
    db_host = "db"
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PW")
    db_name = os.environ.get("DB_NAME")

    while True:
        try:
            MySQLdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
            print("Database is ready!")
            break
        except MySQLdb.Error:
            print("Database is not ready. Waiting...")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db()