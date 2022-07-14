import os
import json


def read_secrets() -> dict:
    filename = os.path.join('C:/Users/Johan/Desktop/MasterProject/MasterProject/secrets.json')
    try:
        with open(filename, mode='r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}


secrets = read_secrets()
