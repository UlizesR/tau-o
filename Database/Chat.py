import os
import psycopg2
from dotenv import load_dotenv

import Database.UserCredentials as uc

load_dotenv()

db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

def create_chat(chat_name, message=None):
    cur.execute("INSERT INTO \"chat\" (session_id, message) VALUES (%s, %s);", (chat_name, message))
    conn.commit()

def get_chats():
    cur.execute("SELECT DISTINCT session_id FROM \"chat\";")
    chats = cur.fetchall()

    if len(chats) == 0:
        print("You have no chats")
        exit()
    
    return chats

def delete_chat(chat_name):
    cur.execute("DELETE FROM \"chat\" WHERE session_id = %s;", (chat_name,))
    conn.commit()
