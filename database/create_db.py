from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()

def create_database():
    database_path = os.getenv('database_path')
    schema_path = os.getenv('schema_path')

    try:
        with open(schema_path, 'r') as file:
            content = file.read()

        con = sqlite3.connect(database_path)
        cur = con.cursor()
        cur.executescript(content)
        cur.close()

    except FileNotFoundError:
        print("Problem in finding schema path")

    except:
        print("some error in create_db.py")