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


def getTaste():
    return db_get("select * from TasteStock")


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
    db_get("select pos_line_id from SalesorderLineOnline where online_line_id = {};".format(id))


def insertSalesorderLine(records):
    line_id = db_get("select max(line_id) from SalesOrderLine")[0][0] + 1
    salesorder_id = records["salesorder_id"]
    stock_id = records["stock_id"]
    # get the first item from the list
    stockInfo = getStockByStockId(stock_id)[0]

    sales_tax = "GST"
    sell_ex = stockInfo[18]
    sell_inc = float(sell_ex)*1.1
    print_ex = sell_ex
    print_inc = sell_inc
    quantity = records["quantity"]
    parentline_id = records["line_type"]        # this just indicate the option
    orderline_id = records["parent_line_id"]    # this is the parentline

    if parentline_id == "DISH":
        parentline_id = 0
        orderline_id = line_id
    else:
        if parentline_id == "EXTRA": # TODO FIX BUG
            parentline_id = 1
        if parentline_id == "TASTE":
            parentline_id = 2

        orderline_id = getLineIdByOnlineId(orderline_id)[0][0]

    db_put("insert into SalesOrderLine(line_id, salesorder_id, stock_id, cost_ex, cost_inc, sales_tax, sell_ex, sell_inc, rrp, print_ex, print_inc, quantity, parentline_id, package, [status], orderline_id, staff_id, out_order, hand_writting, size_level, time_ordered) values({}, {}, {}, 0, 0, 'GST', {}, {}, 0, {}, {}, {}, {}, 0, 1, {}, 0, 0, 0, 0, '{}')".format(
        line_id, salesorder_id, stock_id, sell_ex, sell_inc, print_ex, print_inc, quantity, parentline_id, orderline_id, common.tsToTime(common.getCurrentTs())))

    return (salesorder_id, line_id, records["line_id"])


def activateTable(tableId):
    pass


def findPrinter(lineId):
    #get stock Id
    stockId = db_get("select stock_id from SalesOrderLine where line_id = '{}' order by line_id desc;".format(lineId))[0][0]

    # check stock print
    stockPrint = db_get("select * from StockPrint where stock_id = '{}';".format(stockId))
    if(stockPrint):
        for printer in stockPrint:
            goToKitchen(printer, stockId)

    pass

def goToKitchen(printer, stockId):
    
