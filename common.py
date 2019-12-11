import os
import sys
import json
import time
import datetime
import ftplib
import posOperation

# variable that can be found in setting
DB_HOST = ""
DB_USER = ""
DB_PASSWORD = ""
DB = ""
SLEEPTIME = ""
URLPREFIX = ""
PICTUREPATH = ""


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

    with open(r"API_data\setting.json", 'w') as f:
        json.dump(setting, f)


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


def uploadImage():
    f = ftplib.FTP()

    host = "ftp.kidsnparty.com.au"
    port = 21
    f.connect(host, port)
    print(f.getwelcome())

    userName = "​admin@ozwearugg.com.au".strip(u'\u200b')
    password = "122333@Upos".strip(u'\u200b')

    stockList = posOperation.getStockBarcode()
    pictureList = []

    for stock in stockList:
        barcode = stock[0]
        filePath = PICTUREPATH + barcode + ".jpg"

        if os.path.exists(filePath):
            pictureList.append(filePath)

    with ftplib.FTP(host, userName, password) as ftp:
        ftp.cwd("/kidsnpartycom/src/image/tableorder/bbqhot")

        for picture in pictureList:
            with open(picture, 'rb') as file:
                ftp.storbinary("STOR %s" % picture.split("/")[-1], file)


def roundSeconds(dateTimeObject):
    newDateTime = dateTimeObject

    if newDateTime.microsecond >= 500000:
        newDateTime = newDateTime + datetime.timedelta(seconds=1)

    return newDateTime.replace(microsecond=0)
