import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        self.conn = psycopg2.connect(self.db_url)
        self.cur = self.conn.cursor()

    def insert(self, table, columns: any, values: any) -> None:
        self.cur.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")
        self.conn.commit()

    def select(self, table: str, columns: str, where: str = None) -> list:
        if where != None:
            self.cur.execute(f"SELECT {columns} FROM {table} WHERE {where}")
        else:
            self.cur.execute(f"SELECT {columns} FROM {table}")
        return self.cur.fetchall()
    
    def delete(self, table, where: any) -> None:
        self.cur.execute(f"DELETE FROM {table} WHERE {where}")
        self.conn.commit()
        
DB = Database()