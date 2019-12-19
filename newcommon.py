import os
import sys
import json
import time
import datetime
import ftplib
import posOperation


# this is the decorator
def debug(method):
    def wrapper(*args, **kwargs):
        print("Start " + method.__name__ + "...")
        method(*args, **kwargs)
        print("Complete " + method.__name__ + "...")
    return wrapper


def logging(message):
    print(message)
    with open(r"API_data\errorLogging.txt", 'a+') as f:
        f.write(str(datetime.datetime.now()) + "\t" + message)


class Common:
    DB_HOST = None
    DB_USER = None
    DB_PASSWORD = None
    DB = None
    SLEEPTIME = None
    UPLOADSTOCK = None
    URLPREFIX = None
    PICTUREPATH = None
    APPID = None
    KEY = None
    SECRET = None
    SECURE = None
    HOST = None
    PORT = None

    # instance attributes
    def __init__(self):
        if not os.path.exists("./API_data/setting.json"):
            logging("setting file not found")
            sys.exit()
        with open(r"API_data\setting.json", 'r') as f:
            setting = json.load(f)

        print(setting)
        Common.DB_HOST = setting["DB_host"]
        Common.DB_USER = setting["DB_user"]
        Common.DB_PASSWORD = setting["DB_password"]
        Common.DB = setting["DB"]
        Common.SLEEPTIME = setting["sleeptime"]
        Common.UPLOADSTOCK = setting["uploadStock"]
        Common.URLPREFIX = setting["urlPrefix"]
        Common.PICTUREPATH = setting["picturePath"]
        Common.APPID = setting["app_id"]
        Common.KEY = setting["key"]
        Common.SECRET = setting["secret"]
        Common.SECURE = setting["secure"]
        Common.HOST = setting["host"]
        Common.PORT = setting["port"]

        with open(r"API_data\setting.json", 'w') as f:
            json.dump(setting, f)