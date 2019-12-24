import posOperation
import api
import json
import common
import time
import threading
import sys
import requests
from deprecated import deprecated

tablesRecord = {}
salesorderRecords = {}


def getToken():
    pass


# get all the table from db and update it to api
def addTable(tables):
    
    for table in tables:

        # 如果这张桌子没有被记录，记录它
        if table[2] not in tablesRecord:
            tablesRecord[table[2]] = table[3] # tableCode : tableStatus
            isChanged = True
        else:
            # 状态没有发生改变
            if tablesRecord[table[2]] == table[3]:
                isChanged = False
            else:
                tablesRecord[table[2]] = table[3] # tableCode : tableStatus
                isChanged = True

        # 如果这张桌子没有发生变化，则跳过
        if not isChanged:
            continue
        
        startTime = None if not table[6] else common.roundSeconds(table[6]).strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "tableToken": getToken(),
            "tableId": table[0],
            "siteId": table[1],
            "tableCode": table[2],
            "tableStatus": table[3],
            "inactive": table[4],
            "startTime": startTime,
            "seats": table[7]
        }

        api.addTable(data)
        print("table {} has been updated".format(table[0]))
        # print(data)



# get the newest sales order for active table, and update it to api
def findSalesOrder(tableCode=None):
    
    activeOrderIds = []

    # get activate table
    if tableCode:
        activeTables = posOperation.getTableByTableCode(tableCode)
    else:
        activeTables = posOperation.getActiveTable()

    for table in activeTables:
        ordersDetails = posOperation.getOrderDetailByTableCode(table[2])
        for orderDetails in ordersDetails:
            data = {
                "salesorderId": orderDetails[0],
                "salesorderDate": orderDetails[1].strftime('%Y-%m-%d %H:%M:%S'),
                "tableCode": orderDetails[2],
                "subtotal": float(orderDetails[3]),
                "status": orderDetails[4],
                "guestNo": orderDetails[5],
                "staffId": orderDetails[6]
            }
            api.addSalesOrder(data)
            print("salesorder {} has been updated".format(orderDetails[0]))
            activeOrderIds.append(orderDetails[0])

            # 保持一份salesorderId:status在runtime内存里，用来比较订单状态是否发生改变
            salesorderRecords[orderDetails[0]] = orderDetails[4]

    return activeOrderIds


def checkSalesorderRecords(salesorderRecords):    
    toBeDeleted = []
    for salesorderRecord in salesorderRecords:
        orderDetails = posOperation.getOrderDetailBySalesorderId(salesorderRecord)
        # 在订单时空的清空下，会被直接删除
        if len(orderDetails) == 0:
            toBeDeleted.append(salesorderRecord)
            # 使用api，单独删除线上内容的salesorder by salesorder id
            api.deleteSalesOrder(salesorderRecord)
            continue
        
        # 如果订单状态并未发生改变，则跳过
        orderDetails = orderDetails[0]
        if orderDetails[4] == salesorderRecords[salesorderRecord]:
            continue

        data = {
            "salesorderId": orderDetails[0],
            "salesorderDate": orderDetails[1].strftime('%Y-%m-%d %H:%M:%S'),
            "tableCode": orderDetails[2],
            "subtotal": float(orderDetails[3]),
            "status": orderDetails[4],
            "guestNo": orderDetails[5],
            "staffId": orderDetails[6]
        }
        api.addSalesOrder(data)
        print("salesorder {} has been updated".format(orderDetails[0]))

        if orderDetails[4] == 11:
            toBeDeleted.append(salesorderRecord)

    # 把不需要/已经跟新完毕的订单移除内存
    for key in toBeDeleted:
        del salesorderRecords[key]



# find the need line for the required order, and upload it to api
def postSalesorderLine(salesOrderIds, comments=None):
    # 这里要加锁因为这个轮询可能和websocket的请求冲突
    if len(salesOrderIds) == 0:
        return

    lock = threading.Lock()
    with lock:
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
                "lineType": lineType,
                "comments": comments,
                "timeOrdered": item[7].strftime('%Y-%m-%d %H:%M:%S'),
                "staffId": item[8]
            }

            lst.append(data)

        print(lst)
        if lst != []:
            response = api.addSalesorderLine({"rows": lst})
            
            # if success ->
            if response.status_code < 400:
                posOperation.insertSalesorderLineOnline(lines)


def MyRun():
    while True:
        try:
            tables = posOperation.getTable()
            addTable(tables)  # TODO update table when needed
            checkSalesorderRecords(salesorderRecords)
            salesOrderIds = findSalesOrder()
            postSalesorderLine(salesOrderIds)       # post loacl order to server
            print("RoundEnd!")
            time.sleep(common.SLEEPTIME)
        except TimeoutError:
            print("API service connection time out... retry in 10s")
            # time.sleep(common.SLEEPTIME)
        except requests.exceptions.ConnectionError:
            print("API service not connected... retry in 10s")
        except:
            common.logging("Unexpected error:" + sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[0])
            print("Something wrong with API service... retry in 10s")
