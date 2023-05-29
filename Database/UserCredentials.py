import yaml

with open('Database/user_creds.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

USER = data['username']
USER_ID = data['user_id']

INITIALIZED = data['initialized']