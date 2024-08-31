import os
import requests
import json

from dotenv import load_dotenv, find_dotenv

def main():
    load_dotenv(find_dotenv())
    print(os.environ.get("API_ENDPOINT"))

    req = requests.get(os.environ.get("API_ENDPOINT"))

    with open("temp.json", "w") as file:
        file.write(json.dumps(req.json()))


if __name__ == "__main__":
    main()
