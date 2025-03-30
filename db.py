import os
import time
import sqlite3
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from utils import SongDetailFetcher

load_dotenv(r"./.env")

DB_NAME = os.getenv("PF_DB_NAME")
COLLECTION_NAME = os.getenv("PF_COLLECTION_NAME")

uri = os.getenv("PF_MONGO_STRING")
client = MongoClient(uri, server_api=ServerApi("1"))
db = client.get_database(DB_NAME)
user = db.get_collection(f"{COLLECTION_NAME}")

def get_data():
    conn = sqlite3.connect(f'{DB_NAME}.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {COLLECTION_NAME}")
    rows = cursor.fetchall()
    conn.close()
    
    return rows

def update_local_db(data):
    data['time'] = round(time.time())
    
    try:
        conn = sqlite3.connect(f'{DB_NAME}.db')
        cursor = conn.cursor()

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {COLLECTION_NAME} (time INTEGER, song TEXT, artist TEXT, url TEXT, thumbnail TEXT)")
        cursor.execute(f"INSERT INTO {COLLECTION_NAME} (time, song, artist, url, thumbnail) VALUES (?, ?, ?, ?, ?)",
                       (data['time'], data['song'], data['artist'], data['url'], data['thumbnail']))
        conn.commit()
        conn.close()
        
        print("Local DB updated successfully!")
        return True, "Success"

    except Exception as e:
        print(f"Error updating local DB: {e}")
        return False, e

def update_remote_db(data):
    data['time'] = round(time.time())
    data.pop("thumbnail", None)
    
    try:
        user.insert_one(data)
        print("Remote DB updated successfully!")
        return True, "Success"
    
    except Exception as e:
        print(f"Error updating remote DB: {e}")
        return False, e

if __name__=="__main__":
    a = SongDetailFetcher()
    test_data = a.get_details("https://music.youtube.com/watch?v=Ydv6usKn2rg&list=RDAMVMYdv6usKn2rg")

    update_local_db(test_data)
    update_remote_db(test_data)
    
    time, name, artist, url, thumbnail = get_data()[-1]
    print(time, name, artist, url)