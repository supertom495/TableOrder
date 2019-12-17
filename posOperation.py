import pymssql
import common
import datetime


def db_get(query):
    # Func db_get: Get data from DB.
    try:
        conn = pymssql.connect(host=common.DB_HOST, user=common.DB_USER,
                               password=common.DB_PASSWORD, database=common.DB, charset='utf8')
        cursor = conn.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        # print(res)
        conn.commit()
    except Exception as ex:
        conn.rollback()
        raise ex
    finally:
        conn.close()
    return res


def db_put(query):
    # Func db_get: Get data from DB.
    try:
        conn = pymssql.connect(host=common.DB_HOST, user=common.DB_USER,
                               password=common.DB_PASSWORD, database=common.DB, charset='utf8')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except Exception as ex:
        conn.rollback()
        raise ex
    finally:
        conn.close()


def getOrders(salesOrderId):
    return db_get(
        "select salesorder_id from SalesOrder where salesorder_id > {} order by salesorder_id asc".format(salesOrderId))


def getOrderLines(orderId):
    return db_get("select * from SalesOrderLine where salesorder_id = {};".format(orderId))


def getStock():
    return db_get("select * from Stock order by stock_id;")


def getStockByStockId(stockId):
    return db_get("select * from Stock where stock_id = {};".format(stockId))


def getStockBarcode():
    return db_get("select barcode from Stock")


def getExtra():
    return db_get("select * from ExtraStock")


def findCategoryEnglish(categoryName):
    return db_get("select cat_name2 from Category where cat_name = '{}';".format(categoryName))

def getCategoryId(categoryName):
    return db_get("select cat_id from Category where cat_name = '{}';".format(categoryName))

def getTaste():
    return db_get("select * from TasteStock")

def getKbIdFromKeyboardItem(stockId):
    return db_get("select kb_id from KeyboardItem where stock_Id = {};".format(stockId)) 

def getKbIdFromKeyboardCat(catId):
    return db_get("select kb_id from KeyboardCat where cat_Id = {};".format(catId)) 


def getStockDateModified():
    return db_get("Select stock_id, date_modified from Stock")


def insertStockLastTimeModified(stockId, dateModified):
    db_put(
        "insert into StockLastTimeModified VALUES ({}, '{}');".format(stockId, dateModified))


def getStockDateModifiedAndLastTimeModified():
    return db_get("select s.stock_id, s.date_modified, sltm.date_last_time_modified from Stock as s join StockLastTimeModified as sltm on s.stock_id = sltm.stock_id;")


def updateStockLastTimeModified(stockId, datetime):
    return db_put("update StockLastTimeModified set date_last_time_modified = '{}' where stock_id = {};".format(datetime, stockId))


def getKeyboard():
    return db_get("select kb_id, kb_name from Keyboard")


def getKeyboardCat():
    return db_get("select kb_id, cat_name from KeyboardCat")


def getTable():
    return db_get("select table_id, site_id, table_code, table_status, inactive, logon_time, start_time from [Tables]")

def getTableByTableCode(tableCode):
    return db_get("select table_id, site_id, table_code, table_status, inactive, logon_time, start_time from [Tables] where table_code = '{}';".format(tableCode))

def getActiveTable():
    return db_get("select * from [Tables] where table_status = 2;")


def getActiveSaleOrders():
    return db_get("select custom as table_code, MAX(salesorder_date) as salesorder_date from SalesOrder where custom in (select table_code COLLATE database_default from [Tables] where table_status = 2) group by custom order by custom;")


def getOrderByOrderId(orderId):
    return db_get("select * from SalesOrder where salesorder_id = {};".format(orderId))


def getOrderDetail(tableCode, date):
    return db_get("select salesorder_id, salesorder_date, custom, subtotal, [status] from SalesOrder where custom='{}' and salesorder_date='{}'".format(tableCode, date))


def getSalesOrderIdLinesBySalesOrderId(ids):
    return db_get("select line_id, salesorder_id, stock_id, print_ex, quantity, orderline_id, parentline_id from SalesOrderLine where salesorder_id in {} and line_id not in (select pos_line_id from SalesOrderLineOnline);".format(ids))


# use upload
def insertSalesorderLineOnline(lines):
    query = ""
    for item in lines:
        query += "insert into SalesorderLineOnline (salesorder_id, pos_line_id, online_line_id) values ({}, {}, null);".format(
            item[1], item[0])

    db_put(query)


def insertSalesorderLineOnlineSingle(salesorder_id, pos_line_id, online_line_id):
    query = "insert into SalesorderLineOnline (salesorder_id, pos_line_id, online_line_id) values ({}, {}, {});".format(
        salesorder_id, pos_line_id, online_line_id)

    db_put(query)


def getLineIdByOnlineId(id):
    return db_get("select pos_line_id from SalesorderLineOnline where online_line_id = {};".format(id))


def getSalesOrder(salesOrderId):
    return db_get("select * from SalesOrder where salesorder_id = '{}'".format(salesOrderId))


def insertSalesorderLine(item, salesorderId):
    line_id = db_get("select max(line_id) from SalesOrderLine")[0][0] + 1
    salesorder_id = salesorderId
    stock_id = item["stockId"]
    # get the first item from the list
    stockInfo = getStockByStockId(stock_id)[0]

    sales_tax = "GST"
    sell_ex = stockInfo[18]
    sell_inc = float(sell_ex)*1.1
    print_ex = sell_ex
    print_inc = sell_inc
    quantity = item["quantity"]
    # 2-extra 1-taste 0-dish
    parentline_id = 0        # this just indicate the option  
    orderline_id = line_id    # this is the parentline
    currentTime = common.tsToTime(common.getCurrentTs())

    query = ""
    query += "insert into SalesOrderLine(line_id, salesorder_id, stock_id, cost_ex, cost_inc, sales_tax, sell_ex, sell_inc, rrp, print_ex, print_inc, quantity, parentline_id, package, [status], orderline_id, staff_id, out_order, hand_writting, size_level, time_ordered) values({}, {}, {}, 0, 0, 'GST', {}, {}, 0, {}, {}, {}, {}, 0, 1, {}, 0, 0, 0, 0, '{}');".format(
        line_id, salesorder_id, stock_id, sell_ex, sell_inc, print_ex, print_inc, quantity, parentline_id, orderline_id, currentTime)

    stockTaste = item["stockTaste"]
    stockExtra = item["stockExtra"]
    for stock_id in stockTaste:
        line_id += 1
        taste = 1
        query += "insert into SalesOrderLine(line_id, salesorder_id, stock_id, cost_ex, cost_inc, sales_tax, sell_ex, sell_inc, rrp, print_ex, print_inc, quantity, parentline_id, package, [status], orderline_id, staff_id, out_order, hand_writting, size_level, time_ordered) values({}, {}, {}, 0, 0, 'GST', 0, 0, 0, 0, 0, 1, {}, 0, 1, {}, 0, 0, 0, 0, '{}');".format(
        line_id, salesorder_id, stock_id, taste, orderline_id, currentTime)
    
    for stock_id in stockExtra:
        line_id += 1
        extra = 2
        query += "insert into SalesOrderLine(line_id, salesorder_id, stock_id, cost_ex, cost_inc, sales_tax, sell_ex, sell_inc, rrp, print_ex, print_inc, quantity, parentline_id, package, [status], orderline_id, staff_id, out_order, hand_writting, size_level, time_ordered) values({}, {}, {}, 0, 0, 'GST', 0, 0, 0, 0, 0, 1, {}, 0, 1, {}, 0, 0, 0, 0, '{}');".format(
        line_id, salesorder_id, stock_id, extra, orderline_id, currentTime)

    db_put(query)

    return (salesorder_id, orderline_id)


def activateTable(tableCode):
    return db_put("update [Tables] set table_status = 2, start_time = '{}' where table_code = '{}';".format(common.tsToTime(common.getCurrentTs()), tableCode))

def getStockPrint(stockId):
    return db_get("select * from StockPrint where stock_id = {};".format(stockId))

def getCatPrint(catId):
    return db_get("select * from CatPrint where cat_id = {};".format(catId))

def getKeyboardPrint(kbId):
    return db_get("select * from KeyboardPrint where kb_id = {};".format(kbId))

def getSalesorderLine(lineId):
    return db_get("select * from SalesOrderLine where line_id = '{}';".format(lineId)) 


def findPrinter(lineId):
    #get stock Id from salesorderLine
    salesorderLine = getSalesorderLine(lineId)
    
    stockId = salesorderLine[0][2]
    salesorderId = salesorderLine[0][1]
    salesOrder = getSalesOrder(salesorderId)
    stock = getStockByStockId(stockId)

    # check stock print
    stockPrint = getStockPrint(stockId)
    if(stockPrint):
        goToKitchen(stockPrint, salesorderLine, salesOrder, stock)
        return 


    # check cat print
    catName = stock[0][13]
    catId = getCategoryId(catName)[0][0]
    catPrint = getCatPrint(catId)
    if(catPrint):
        goToKitchen(catPrint, salesorderLine, salesOrder, stock)
        return


    # check keyboard print
    kbId = getKbIdFromKeyboardItem(stockId)
    # 如果不在keyboard item 里面， 就去keyboard 里面找
    if (not kbId): 
        kbId = getKbIdFromKeyboardCat(catId)
    kbId = kbId[0][0]
    keyboardPrint = getKeyboardPrint(kbId)
    if(keyboardPrint):
        goToKitchen(keyboardPrint, salesorderLine, salesOrder, stock)
        return

def goToKitchen(printers, salesorderLine, salesOrder, stock):
    query = ""
    for printer in printers:
        lineId = salesorderLine[0][0]
        salesorderId = salesorderLine[0][1]
        tableCode = salesOrder[0][7]
        cat1 = stock[0][13]
        description = stock[0][11]
        description2 = stock[0][35]
        quantity = salesorderLine[0][11]
        order_time = salesorderLine[0][18]
        cat2 = stock[0][14]
        printerName = printer[2]
        comments = "some comments"

        query += "INSERT INTO [RPOS1].[dbo].[Kitchen] ([line_id], [orderline_id], [table_code], [staff_name],[cat1],[description],[description2],[unit],[quantity],[printer],[printer2],[order_time],[handwritting],[comments],[stock_type],[out_order],[customer_name],[cat2],[salesorder_id],[status],[original_line_id])VALUES('{}','{}','{}','oneline','{}','{}','{}','1', {},'{}','{}','{}',0, '{}', '0','0','{}','{}', {},null,null);".format(lineId, lineId, tableCode, cat1, description, description2, quantity, printerName, printerName, order_time, comments, tableCode, cat2, salesorderId)

    db_put(query)