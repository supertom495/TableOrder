import os
import sys
import json
import time
import datetime
import posOperation
import threading

# variable that can be found in setting
DB_HOST = ""
DB_USER = ""
DB_PASSWORD = ""
DB = ""
SLEEPTIME = ""
URLPREFIX = ""
PICTUREPATH = ""
APPID = ""
KEY = ""
SECRET = ""
SECURE = False
HOST = ""
PORT = -1

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


@debug
def setVar():
    setting = {}
    global DB_HOST
    global DB_USER
    global DB_PASSWORD
    global DB
    global SLEEPTIME
    global URLPREFIX
    global PICTUREPATH
    global APPID
    global KEY
    global SECRET
    global SECURE
    global HOST
    global PORT
    
    if not os.path.exists("./API_data/setting.json"):
        logging("setting file not found")
        sys.exit()
    with open(r"API_data\setting.json", 'r') as f:
        setting = json.load(f)

    print(setting)
    DB_HOST = setting["DB_host"]
    DB_USER = setting["DB_user"]
    DB_PASSWORD = setting["DB_password"]
    DB = setting["DB"]
    SLEEPTIME = setting["sleeptime"]
    UPLOADSTOCK = setting["uploadStock"]
    URLPREFIX = setting["urlPrefix"]
    PICTUREPATH = setting["picturePath"]
    APPID = setting["app_id"]
    KEY = setting["key"]
    SECRET = setting["secret"]
    SECURE = setting["secure"]
    HOST = setting["host"]
    PORT = setting["port"]

    with open(r"API_data\setting.json", 'w') as f:
        json.dump(setting, f)

@debug
def setUpTable():
    posOperation.dropTableAndCreateSalesorderLineOnline()

@debug
def setUpWebsocketServer():
    t = threading.Thread(target=runWebsocket)
    t.setDaemon(True)
    t.start()
    print("wait...10s" + "setting up websocket connection")
    time.sleep(10)


def runWebsocket():
    import subprocess
    filepath=r"API_data\start_websockets.bat"
    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
    stdout, stderr = p.communicate()
    print (p.returncode) # is 0 if success


# format match the api requirement
def getCurrentTs():
    return int(round(time.time()))


def readStockTimestamp():
    # get the time last update stock online
    if not os.path.exists("./API_data/setting.json"):
        print("setting file not found")
        sys.exit()

    with open(r"API_data\setting.json", 'r') as f:
        setting = json.load(f)
        timestamp = setting["timestampStock"]

    return int(timestamp)


def recordStockTimestamp():

    with open(r"API_data\setting.json", 'r') as f:
        setting = json.load(f)
    with open(r"API_data\setting.json", 'w') as f:
        setting["timestampStock"] = getCurrentTs()
        json.dump(setting, f)


def recordTheOrderId(Id):
    # write the num to the local txt file
    with open(r"API_data\recordedOrderId.txt", 'w') as f:
        f.write(str(Id))


def tsToTime(ts):
    ts = int(ts)
    # ts /= 1000
    t = time.localtime(ts)
    docketDate = time.strftime("%Y-%m-%d %H:%M:%S", t)
    # docketDate += ".000"
    return docketDate


def roundSeconds(dateTimeObject):
    newDateTime = dateTimeObject

    if newDateTime.microsecond >= 500000:
        newDateTime = newDateTime + datetime.timedelta(seconds=1)

    return newDateTime.replace(microsecond=0)
