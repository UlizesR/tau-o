import yaml

with open("creds.yaml", "r") as f:
    creds = yaml.load(f, Loader=yaml.FullLoader)

USER = creds["username"]
PASSWORD = creds["password"]
EMAIL = creds["email"]
USER_ID = creds["user_id"]

INITIALIZED = creds["initialized"]