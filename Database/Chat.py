import os
import psycopg2
import halo
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
    with halo.Halo(text='Querying chats', spinner='simpleDots'):
        cur.execute("SELECT DISTINCT session_id FROM \"chat\";")
        chats = cur.fetchall()

    if len(chats) == 0:
        print("You have no chats")
        exit()
    
    return chats

def get_chat(chat_name):
    with halo.Halo(text=f'Getting {chat_name} chat.', spinner='simpleDots'):
        cur.execute("SELECT * FROM \"chat\" WHERE session_id = %s;", (chat_name,))
        chat = cur.fetchall()

    if len(chat) == 0:
        print("Chat not found")
        exit()
    
    return chat

def delete_chat(chat_name):
    with halo.Halo(text='Deleting chat', spinner='simpleDots'):
        cur.execute("DELETE FROM \"chat\" WHERE session_id = %s;", (chat_name,))
        conn.commit()
    print(f"{chat_name} has been deleted")