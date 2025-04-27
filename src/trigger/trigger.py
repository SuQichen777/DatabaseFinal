import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pymysql
from pymysql.constants import CLIENT
from config import Config
from pathlib import Path


def trigger():
    db = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
        client_flag=CLIENT.MULTI_STATEMENTS
    )

    cursor = db.cursor()
    if db.open:
        print("Database connection established.")
    else:
        print("Failed to connect to the database.")
        return

    sql_file_path = Path(__file__).parent / "trigger.sql"
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        sql_commands = file.read()

    try:
        cursor.execute(sql_commands) 

        while cursor.nextset():
            pass

        print("trigger.sql executed successfully.")
    except pymysql.MySQLError as err:
        print(f"Error executing SQL script:\n{err}")

    db.commit()
    cursor.close()
    db.close()


if __name__ == "__main__":
    trigger()
