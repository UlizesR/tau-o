import os
import psycopg2
import yaml
from dotenv import load_dotenv

import Database.UserCredentials as uc

load_dotenv()

class Auth:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        self.cur = self.conn.cursor()
        with open("Database/user_creds.yaml", "r") as file:
            self.data = yaml.safe_load(file)

    def login_verification(self, username, password):
        # Check if user is already initialized
        if uc.INITIALIZED:
            print("User is already innitialized.")
            exit()

        # Check if user exists in database
        self.cur.execute("SELECT * FROM \"User\" WHERE username = %s AND password = %s;", (username, password))
        user = self.cur.fetchall()
        if user:
            # Set user to be initialized in the user_creds.yaml file
            self.data = {
                'initialized': True,
                'email': user[0][1],
                'username': username,
                'user_id': user[0][0],
                'password': password
            }
            with open("Database/user_creds.yaml", "w") as file:
                yaml.dump(self.data, file)

            print("User has been initialized.")
            exit()
        print("User not found.")
        print("Please verify your credentials.")
        exit()


    def register(self, email, username, password):
        # Check if user is already initialized
        if uc.INITIALIZED:
            print("User is already innitialized.")
            exit()

        # Check if user already exists in database
        self.cur.execute("SELECT * FROM \"User\" WHERE username=%s OR email=%s;", (username, email))
        user_exist = self.cur.fetchall()
        if user_exist:
            print("User with given email or username already exists.")
            exit()

        # Insert user into database
        self.cur.execute("INSERT INTO \"User\" (email, username, password) VALUES (%s, %s, %s);", (email, username, password))
        self.conn.commit()
        self.cur.execute("SELECT * FROM \"User\" WHERE username=%s;", (username,))
        user = self.cur.fetchall()

        # Set user to be initialized in the user_creds.yaml file
        self.data = {
            'initialized': True,
            'email': email,
            'username': username,
            'user_id': user[0][2],
            'password': password
        }
        with open("Database/user_creds.yaml", "w") as file:
            yaml.dump(self.data, file)

        print("User has been created and initialized.")
        exit()