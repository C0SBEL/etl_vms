import json
import requests

url = "https://randomuser.me/api/?results=5000"

def getRandomUsers():
    try:
        response = requests.get(url)
        response.raise_for_status()
        users = response.json()
        print(users)
        return users
    except Exception as e:
        print(e)
        return {}


if __name__ == "__main__":
    users = getRandomUsers()