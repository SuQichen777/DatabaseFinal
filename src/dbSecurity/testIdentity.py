import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pymysql
from config import Config
from pathlib import Path


def testIdentity():
    db = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
    )

    cursor = db.cursor()
    # Check if the connection was successful
    if db.open:
        print("Database connection established.")
    else:
        print("Failed to connect to the database.")
        return


    # read insertData.sql file
    insert_file_path = Path(__file__).parent / "testIdentity.sql"
    with open(insert_file_path, 'r', encoding='utf-8') as file:
        insert_commands = file.read()
    # Split the SQL commands by semicolon
    insert_commands = insert_commands.split(';')
    for command in insert_commands:
        command = command.strip()
        if command:
            try:
                cursor.execute(command)
            except pymysql.MySQLError as err:
                print(f"If you are a developer, there is a problem with the testIdentity.sql file. If you are a user, it is normal to see this error. \nError executing command: {command}\n{err}")

    # Commit the changes
    print("TestDB Successfully Inserted")
    db.commit()
    cursor.close()
    db.close()
    

if __name__ == "__main__":
    testIdentity()
