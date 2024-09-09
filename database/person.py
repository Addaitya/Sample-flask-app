from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()

database_path = os.getenv('database_path')


def fetch_person(id: int):
    con = sqlite3.connect(database_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    try:
        query = '''
            select * from persons where id = :id;
        '''

        res = cur.execute(query, {"id": id})

        data = res.fetchone()
        data = {key: data[key] for key in data.keys()}
        con.close()
        return data

    except Exception as e:
        print(f"Error in fetch_person: \n{e}")
        return {}

def fetch_people():
    con = sqlite3.connect(database_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    query = '''
        select * from persons;
    '''
    try:
        res = cur.execute(query)
        data = res.fetchall()
        data = [{key: row[key] for key in row.keys()} for row in data]
        con.close()
        return data
    
    except Exception as e:
        print(f"Error in get_persons: \n{e}")
        return []

def append_person(row):
    con = sqlite3.connect(database_path)
    cur = con.cursor()

    query = '''
        insert into persons(name, age) values(:name, :age);
    '''

    try:
        cur.execute(query, row)
        last_row_id = cur.lastrowid
        con.commit()
        con.close()

        return {"id": last_row_id}

    except Exception as e:
        print(f"Error in append_person: {e}")
        return {}
    
def add_image_name(id, filename):
    con = sqlite3.connect(database_path)
    cur = con.cursor()

    query = '''
        update persons set photo_id = :filename where id = :id; 
    '''
    try: 
        cur.execute(query, {"id": id, "filename": filename})
        con.commit()
        con.close()
        return True
    
    except Exception as e:
        print("Error in add_image_name: \n{e}")
        return False