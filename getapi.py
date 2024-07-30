import os
from dotenv import load_dotenv

def get_api():
    load_dotenv()
    return os.environ["API_KEY"]

def get_slave_ip()
    load_dotenv()
    return os.environ["SLAVE_IP"]

def get_slave_port()
    load_dotenv()
    return os.environ["SLAVE_PORT"]

def get_master_ip()
    load_dotenv()
    return os.environ["MASTER_IP"]

def get_master_port()
    load_dotenv()
    return os.environ["MASTER_PORT"]

if __name__ == "__main__":
    print("api : ", get_api()
    print("slave ip : ", get_slave_ip())
    print("slave port : ", get_slave_port())
    print("master ip : ", get_master_ip())
    print("master port : ", get_master_port())

