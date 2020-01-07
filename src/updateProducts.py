import posOperation
from datetime import datetime
import common
import api
import time
import ftplib
import os
import pollingDatabase


def updateKeyboard():
    keyboard = posOperation.getKeyboard()
    keyboardCat = posOperation.getKeyboardCat()

    lst = []
    for item in keyboard:
        if item[1] is '': continue
        lst.append({"kbId": item[0], "kbName": item[1]})
    print(lst)
    api.addKeyboard({"rows": lst})

    lst = []
    for item in keyboardCat:
        if item[1] is '': continue
        lst.append({
            "kbId": item[0],
            "catName": item[1],
            "catId": item[2]
        })
    print(lst)
    api.addKeyboardCat({"rows": lst})


def updateKeyboardItem():
    keyboardItem = posOperation.getKeyboardItem()

    lst = []
    for item in keyboardItem:
        if item[4] is '': continue
        lst.append({
            "kbId": item[0],
            "itemName": item[1],
            "catId": item[2],
            "itemId": item[3],
            "itemBarcode": item[4],
            "stockId": item[5]
        })
    print(lst)
    api.addKeyboardItem({"rows": lst})


def castStock(stock):
    cat1En = posOperation.findCategoryEnglish(stock[13])
    cat2En = posOperation.findCategoryEnglish(stock[14])
    cat1En = cat1En[0][0] if cat1En != [] else ""
    cat2En = cat2En[0][0] if cat2En != [] else ""

    data = {
        "stockId": stock[0],
        "barcode": stock[1],
        "custom1": stock[2],
        "custom2": stock[3],
        "salesPrompt": stock[4],
        "description1": stock[11],
        "description2": stock[34],
        "longdesc": stock[12],
        "cat1": stock[13],
        "cat1En": cat1En,
        "cat2": stock[14],
        "cat2En": cat2En,
        "price": float(stock[18]) * 1.1,
        "quantity": stock[19]
    }
    return data


def castOption(table, rows):
    data = {
        "table": table,
        "rows": rows
    }
    return data


def updateStock():
    result = posOperation.getStock()  # get all stock in the list

    recordedDate = datetime.fromtimestamp(common.readStockTimestamp())
    common.recordStockTimestamp()
    for stock in result:
        # find if the stock has any change
        modifiedDate = stock[29]

        if (modifiedDate > recordedDate):
            print("Uploading stock: " + str(stock[0]))

            response = api.addStock(castStock(stock))

            if (response.status_code == 200):
                print("successfully uploaded")
            else:
                print("error code: " + str(response.status_code))
                print("error content: " + response.text)


def updateStaff():
    result = posOperation.getStaff()
    for staff in result:
        data = {
            "staffId": staff[0],
            "barcode": staff[1],
            "inactive": staff[2],
            "surname": staff[3],
            "givenNames": staff[4]
        }
        api.addStaff(data)
        print("Staff: {} added".format(staff[0]))


def updateProducts():
    # upload Stock
    updateStock()

    # upload keyboard
    updateKeyboard()

    # update keyboardItem
    updateKeyboardItem()

    # upload extra to api
    result = posOperation.getExtra()
    response = api.addOption(castOption("stock_extra", result))
    print("Extra: " + response.text)

    # upload taste to api
    result = posOperation.getTaste()
    response = api.addOption(castOption("stock_taste", result))
    print("Taste: " + response.text)

    # upload image
    uploadImageToAPI()

    updateStaff()

    # delete all the table online
    api.deleteTable()

    pollingDatabase.tablesRecord = {}

    time.sleep(2)


def uploadImageToFTP():
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
        filePath = common.PICTUREPATH + barcode + ".jpg"

        if os.path.exists(filePath):
            pictureList.append(filePath)

    with ftplib.FTP(host, userName, password) as ftp:
        ftp.cwd("/kidsnpartycom/src/image/tableorder/bbqhot")

        for picture in pictureList:
            with open(picture, 'rb') as file:
                ftp.storbinary("STOR %s" % picture.split("/")[-1], file)


def uploadImageToApache():
    from distutils.dir_util import copy_tree

    # copy subdirectory example
    fromDirectory = common.PICTUREPATH
    toDirectory = "c:/xampp/htdocs/my_assets/images"
    copy_tree(fromDirectory, toDirectory)


def uploadImageToAPI():
    stockList = posOperation.getStockBarcode()
    pictureList = []

    for stock in stockList:
        barcode = stock[0]
        filePath = common.PICTUREPATH + barcode + ".jpg"

        if os.path.exists(filePath):
            pictureList.append(filePath)

    for picture in pictureList:
        with open(picture, 'rb') as file:
            data = {
                "fileName": picture.split("/")[-1]
            }
            api.uploadStockImage(data, file)
