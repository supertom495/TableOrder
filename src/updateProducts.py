import posOperation
from datetime import datetime
import common
import api
import time


def updateKeyboard():
    keyboard = posOperation.getKeyboard()
    keyboardCat = posOperation.getKeyboardCat()

    lst = []
    for item in keyboard:
        lst.append({"kbId": item[0], "kbName": item[1]})
    print(lst)
    api.addKeyboard({"rows": lst})

    lst = []
    for item in keyboardCat:
        lst.append({"kbId": item[0], "catName": item[1]})
    print(lst)
    api.addKeyboardCat({"rows": lst})

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
        "price": float(stock[18])*1.1,
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



def updateProducts():

    # upload Stock
    updateStock()

    # upload extra to api
    result = posOperation.getExtra()
    response = api.addOption(castOption("stock_extra", result))
    print("Extra: " + response.text)

    # upload taste to api
    result = posOperation.getTaste()
    response = api.addOption(castOption("stock_taste", result))
    print("Taste: " + response.text)

    # upload image to api
    common.uploadImage()

    # upload keyboard
    updateKeyboard()

    time.sleep(2)

