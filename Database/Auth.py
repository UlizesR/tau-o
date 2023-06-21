import yaml

from Database.Query import DB 
import Database.UserCreds as uc 

class Auth:
    def __init__(self):
        with open("creds.yaml", "r") as f:
            self.creds = yaml.safe_load(f)

    def login(self, username: str, password: str) -> None:
        """
            Login a user
            Params:
                username: str
                password: str

            Returns:
                None
        """
        # first check if user has already been initialized
        if uc.INITIALIZED:
            print("User is already initialized!")
            exit()
        
        # check if user exists
        data = DB.select("users", "username", f"username = '{username}'")

        # if user does not exist, raise an exception
        if not data:
            raise Exception("User not found")
        
        # check if password is correct
        if not data[0][1] == password:
            raise Exception("Password is incorrect")
        
        # if user exists and password is correct, initialize user
        self.creds = {
            'username': username,
            'password': password,
            'email': data[0][2],
            'user_id': data[0][0],
            'initialized': True
        }

        # write to creds.yaml
        with open("creds.yaml", "w") as f:
            yaml.dump(self.creds, f)

        # print success message
        print("Logged in successfully!\n")
        print("User initialized successfully!")

        exit()
            
    def register(self, username: str, password: str, email: str) -> None:
        """
            Register a new user
            Params:
                username: str
                password: str
                email: str

            Returns:
                None
        """
        # first check if user has already been initialized
        if uc.INITIALIZED:
            print("User is already initialized!")
            exit()
        
        # check if user exists
        data = DB.select("users", "username", f"username = '{username}'")

        # if user exists, raise an exception
        if data:
            raise Exception("User already exists")
        
        # if user does not exist, insert user into database
        DB.insert("users", "username, password, email", f"'{username}', '{password}', '{email}'")

        # get user_id
        data = DB.select("users", "id", f"username = '{username}'")
        user_id = data[0][0]

        # initialize user
        self.creds = {
            'username': username,
            'password': password,
            'email': email,
            'user_id': user_id,
            'initialized': True
        }

        # write to creds.yaml
        with open("creds.yaml", "w") as f:
            yaml.dump(self.creds, f)

        # print success message
        print("Registered successfully!\n")
        print("User initialized successfully!")

        exit()