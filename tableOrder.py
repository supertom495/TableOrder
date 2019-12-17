import json
import pymssql
import time
import common
import posOperation
import threading
import tkinter as tk
import tkinter.font as tkFont
import api
from datetime import datetime
import pysher
import sys
import logging
import pusher
from deprecated import deprecated

def getToken():
    pass

# get all the table from db and update it to api


def addTable(tables):
    
    for item in tables:
        data = {
            "tableToken": getToken(),
            "tableId": item[0],
            "siteId": item[1],
            "tableCode": item[2],
            "tableStatus": item[3],
            "inactive": item[4],
            "startTime": common.roundSeconds(item[6]).strftime('%Y-%m-%d %H:%M:%S')
        }

        api.addTable(data)
        print("table {} has been updated".format(item[0]))
        # print(data)


# get the newest sales order for active table, and update it to api
def findSalesOrder():
    activeOrders = posOperation.getActiveSaleOrders()
    activeOrderIds = []
    for item in activeOrders:
        orderDetails = posOperation.getOrderDetail(item[0], item[1])[0]
        data = {
            "salesorderId": orderDetails[0],
            "salesorderDate": orderDetails[1].strftime('%Y-%m-%d %H:%M:%S'),
            "tableCode": orderDetails[2],
            "subtotal": float(orderDetails[3]),
            "status": orderDetails[4]
        }
        api.addSalesOrder(data)
        print("salesorder {} has been updated".format(orderDetails[0]))
        activeOrderIds.append(orderDetails[0])

    return activeOrderIds

    # print(orderDetails)


# find the need line for the required order, and upload it to api
def postSalesorderLine(salesOrderIds):
    ids = str(tuple(salesOrderIds))
    if len(salesOrderIds) == 1:
        ids = ids.replace(",", "")
    lines = posOperation.getSalesOrderIdLinesBySalesOrderId(ids)
    lst = []

    for item in lines:
        if item[6] == 0:
            lineType = "DISH"
        if item[6] == 1:
            lineType = "TASTE"
        if item[6] == 2:
            lineType = "EXTRA"

        data = {
            "posLineId": item[0],
            "salesorderId": item[1],
            "stockId": item[2],
            "price": float(item[3]),
            "quantity": item[4],
            "parentLineId": item[5],
            "lineType": lineType
        }

        lst.append(data)

    print(lst)
    if lst != []:
        api.addSalesorderLine({"rows": lst})
    # if success ->
    posOperation.insertSalesorderLineOnline(lines)

@deprecated(version='0.1', reason="You should use add_dish, which is the callback of websockets")
def processOnlineSalesorderLine(lines):
    # try to insert into salesorderline first,
    # if success, write it to SalesorderLineOnline
    # then tell server this operation is succeed
    # is not success, the orderline will be found in the next round
    successList = []
    for item in lines["salesorderlines"]:
        result = posOperation.insertSalesorderLine(item)
        posOperation.insertSalesorderLineOnlineSingle(
            result[0], result[1], result[2])  # salesorder_id, pos_line_id, online_line_id
        successList.append([result[2], result[1]])
        print("DISH: \n" + 
        "salesorder_id, pos_line_id, online_line_id\n {} added\n".format(result))

    api.updateSalesorderLine({"rows": successList})


# retrive online orderline, and write it to POS
@deprecated(version='0.1', reason="You should use websocket instead")
def retriveSalesorderLine(salesOrderIds):
    response = api.getSalesorderLine(salesOrderIds)
    result = json.loads(response.text)
    # for item in result:
    processOnlineSalesorderLine(result)


def checkStock(button, buttontext):
    buttontext.set("Updating")
    button.config(state="disabled")
    button.update()

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
    buttontext.set("update stock")
    button.config(state="active")
    button.update()


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


def open_table(data, *args, **kwargs):
    print("processing Args:", args)
    print("processing Kwargs:", kwargs)
    print("Channel Callback: %s" % data)
    print("Table Opened")
    data = json.loads(data)
    tableCode = data["tableCode"]
    common.setVar()
    posOperation.activateTable(tableCode)
    table = posOperation.getTableByTableCode(tableCode)
    addTable(table)
    sender.trigger('littlenanjing', 'App\\Events\\OpenTableResult', {'tableCode': tableCode,
        'code': '0', 'message':'giao', 'salesorderId':1234})


def add_dish(data, *args, **kwargs):
    print("processing Args:", args)
    print("processing Kwargs:", kwargs)
    print("Channel Callback: %s" % data)
    print("Table Opened")

    data = json.loads(data)

    salesorderId = data["salesorderId"]
    salesorderLines = data["salesorderLines"]
    for item in salesorderLines:
        result = posOperation.insertSalesorderLine(item, salesorderId, dishType=0)

        comments = item["comments"]
        print("DISH: \n" + 
        "line_id\n {} added\n".format(result))

    # successList = []
    # for item in lines["salesorderlines"]:
    #     result = posOperation.insertSalesorderLine(item)
    #     posOperation.insertSalesorderLineOnlineSingle(
    #         result[0], result[1], result[2])  # salesorder_id, pos_line_id, online_line_id
    #     successList.append([result[2], result[1]])
    #     print("DISH: \n" + 
    #     "salesorder_id, pos_line_id, online_line_id\n {} added\n".format(result))

    # api.updateSalesorderLine({"rows": successList})

    
    sender.trigger('littlenanjing', 'App\\Events\\AddDishResult', {'salesorderId': 1234,
        'code': '0', 'message':'success'})


# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
    channel = receiver.subscribe('littlenanjing')
    channel.bind('App\\Events\\OpenTableRequest', open_table)
    channel.bind('App\\Events\\AddDishRequest', add_dish)


def MyRun():
    while True:
        tables = posOperation.getTable()
        addTable(tables)  # TODO update table when needed
        salesOrderIds = findSalesOrder()
        postSalesorderLine(salesOrderIds)       # post loacl order to server
        # retriveSalesorderLine(salesOrderIds)    # download remote orderline
        print("RoundEnd!")
        time.sleep(common.SLEEPTIME)


def thread_it(button, buttontext):
    #     global buttontext
    buttontext.set("Working")
    button.config(state="disabled")
    button.update()
    t = threading.Thread(target=MyRun)
    t.setDaemon(True)
    t.start()



if __name__ == "__main__":


    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    root.addHandler(ch)
    receiver = pysher.Pusher(key="ABCDEF", secure=False, custom_host="192.168.1.26", port="6001")
    sender = pusher.Pusher(app_id='12345', key='ABCDEF', secret='HIJKLMNOP', ssl=False, host='192.168.1.26', port=6001)

    receiver.connection.bind('pusher:connection_established', connect_handler)
    receiver.connect()


    common.setVar()

    window = tk.Tk()
    window.title("Table Order")
    window.geometry('400x400')

    ft = tkFont.Font(family='Fixdsys', size=20, weight=tkFont.BOLD)
    w = tk.Label(window, text="Start plugin.", font=ft).place(x=120, y=160)
    buttontext = tk.StringVar()
    buttontext.set('Start')
    b = tk.Button(window, textvariable=buttontext, font=(
        'Arial', 12), width=10, height=1, command=lambda: thread_it(b, buttontext))
    b.place(x=150, y=230)

    # need a button to sync stock
    syncStockButtonText = tk.StringVar()
    syncStockButtonText.set("update stock")

    syncStockButton = tk.Button(
        window, textvariable=syncStockButtonText, font=(
            'Arial', 12), width=10, height=1, command=lambda: checkStock(syncStockButton, syncStockButtonText))
    syncStockButton.place(x=150, y=330)

    print("function initialization successful")
    window.mainloop()
