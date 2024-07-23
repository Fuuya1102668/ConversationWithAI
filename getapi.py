import os
from dotenv import load_dotenv

def get_api():
    load_dotenv()
    return os.environ["API_KEY"]

if __name__ == "__main__":
    api = get_api()
    print(api)

