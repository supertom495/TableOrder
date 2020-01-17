import pymssql
import common


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
    return db_get(
        "select s.stock_id, s.date_modified, sltm.date_last_time_modified from Stock as s join StockLastTimeModified "
        "as sltm on s.stock_id = sltm.stock_id;")


def updateStockLastTimeModified(stockId, datetime):
    return db_put(
        "update StockLastTimeModified set date_last_time_modified = '{}' where stock_id = {};".format(datetime,
                                                                                                      stockId))


def getKeyboard():
    return db_get("select kb_id, kb_name from Keyboard")


def getKeyboardByKeyboardName(kbName):
    return db_get("select kb_id from Keyboard where kb_name = '{}'".format(kbName))


def getKeyboardCat():
    return db_get("select kb_id, cat_name, cat_id from KeyboardCat")


def getKeyboardItem():
    return db_get("select kb_id, item_name, cat_id, item_id, item_barcode, stock_id from KeyboardItem")


def getTable():
    return db_get(
        "select table_id, site_id, table_code, table_status, inactive, logon_time, start_time, seats, staff_id from ["
        "Tables]")


def getTableByTableCode(tableCode):
    return db_get(
        "select table_id, site_id, table_code, table_status, inactive, logon_time, start_time, seats, staff_id from ["
        "Tables] where table_code = '{}';".format(
            tableCode))


def getActiveTable():
    return db_get(
        "select table_id, site_id, table_code, table_status, inactive, logon_time, start_time, seats, staff_id from ["
        "Tables] where table_status = 2;")


def getTableStaffId(tableCode):
    return db_get("select staff_id from [Tables] where table_code = '{}';".format(tableCode))


def swapTable(fromTableCode, toTableCode):
    query = ("UPDATE t1 " +
             "SET " +
             "t1.table_status = t2.table_status, " +
             "t1.start_time = t2.start_time " +
             "FROM [Tables] AS t1 " +
             "INNER JOIN [Tables] AS t2 " +
             "    ON      (t1.table_code = '{}' " +
             "            AND t2.table_code = '{}') " +
             "        OR " +
             "            (t1.table_code = '{}' " +
             "            AND t2.table_code = '{}'); ").format(fromTableCode, toTableCode, toTableCode, fromTableCode)
    db_put(query)


def activateTable(tableCode):
    return db_put("update [Tables] set table_status = 2, start_time = '{}' where table_code = '{}';".format(
        common.tsToTime(common.getCurrentTs()), tableCode))


# get latest 2 orders from this table
def getOrderDetailByTableCode(tableCode):
    return db_get(
        "select top 1 salesorder_id, salesorder_date, custom, subtotal, [status], guest_no, staff_id from SalesOrder "
        "where custom='{}' order by salesorder_date desc;".format(tableCode))


# get latest 2 orders from this table
def getOrderDetailBySalesorderId(salesorderId):
    return db_get(
        "select top 1 salesorder_id, salesorder_date, custom, subtotal, [status], guest_no, staff_id from SalesOrder "
        "where salesorder_id={} order by salesorder_date desc;".format(salesorderId))


def getSalesOrderIdLinesBySalesOrderId(ids):
    return db_get(
        "select line_id, salesorder_id, stock_id, print_ex, quantity, orderline_id, parentline_id, time_ordered, "
        "staff_id from SalesOrderLine where salesorder_id in {} and line_id not in (select pos_line_id from "
        "SalesOrderLineOnline) and [status] = 1;".format(ids))


# 找到pos上删掉的菜
def getSalesorderLineOnlineDeleted(ids):
    return db_get(
        "select pos_line_id from SalesorderLineOnline where salesorder_id in {} and pos_line_id not in (select "
        "line_id from SalesOrderLine);".format(ids))


# use upload
def insertSalesorderLineOnline(lines):
    query = ""
    for item in lines:
        query += "insert into SalesorderLineOnline (salesorder_id, pos_line_id, online_line_id) values ({}, {}, null);".format(
            item[1], item[0])
    db_put(query)


def deleteSalesorderLineOnline(lines):
    query = "delete from SalesorderLineOnline where pos_line_id in {};".format(lines)
    db_put(query)


def insertSalesorderLine(item, salesorderId, staffId):
    line_id = db_get("select max(line_id) from SalesOrderLine")
    line_id = 1 if line_id[0][0] is None else line_id[0][0] + 1

    salesorder_id = salesorderId
    stock_id = item["stockId"]
    # get the first item from the list
    stockInfo = getStockByStockId(stock_id)[0]

    sales_tax = "GST"
    sell_ex = stockInfo[18]
    sell_inc = float(sell_ex) * 1.1
    print_ex = sell_ex
    print_inc = sell_inc
    quantity = item["quantity"]
    # 2-extra 1-taste 0-dish
    parentline_id = 0  # this just indicate the option
    orderline_id = line_id  # this is the parentline
    currentTime = common.tsToTime(common.getCurrentTs())

    query = ""
    query += "insert into SalesOrderLine(line_id, salesorder_id, stock_id, cost_ex, cost_inc, sales_tax, sell_ex, " \
             "sell_inc, rrp, print_ex, print_inc, quantity, parentline_id, package, [status], orderline_id, staff_id, " \
             "out_order, hand_writting, size_level, time_ordered) values({}, {}, {}, 0, 0, 'GST', {}, {}, 0, {}, {}, " \
             "{}, {}, 0, 1, {}, {}, 0, 0, 0, '{}');".format(
        line_id, salesorder_id, stock_id, sell_ex, sell_inc, print_ex, print_inc, quantity, parentline_id, orderline_id,
        staffId, currentTime)

    stockTaste = item["stockTaste"]
    stockExtra = item["stockExtra"]
    for stock_id in stockTaste:
        line_id += 1
        taste = 1
        query += "insert into SalesOrderLine(line_id, salesorder_id, stock_id, cost_ex, cost_inc, sales_tax, sell_ex, " \
                 "sell_inc, rrp, print_ex, print_inc, quantity, parentline_id, package, [status], orderline_id, " \
                 "staff_id, out_order, hand_writting, size_level, time_ordered) values({}, {}, {}, 0, 0, 'GST', 0, 0, " \
                 "0, 0, 0, 1, {}, 0, 1, {}, {}, 0, 0, 0, '{}');".format(
            line_id, salesorder_id, stock_id, taste, orderline_id, staffId, currentTime)

    for stock_id in stockExtra:
        line_id += 1
        extra = 2
        query += "insert into SalesOrderLine(line_id, salesorder_id, stock_id, cost_ex, cost_inc, sales_tax, sell_ex, " \
                 "sell_inc, rrp, print_ex, print_inc, quantity, parentline_id, package, [status], orderline_id, " \
                 "staff_id, out_order, hand_writting, size_level, time_ordered) values({}, {}, {}, 0, 0, 'GST', 0, 0, " \
                 "0, 0, 0, 1, {}, 0, 1, {}, {}, 0, 0, 0, '{}');".format(
            line_id, salesorder_id, stock_id, extra, orderline_id, staffId, currentTime)

    db_put(query)

    return salesorder_id, orderline_id, line_id


def getSalesOrder(salesOrderId):
    return db_get("select * from SalesOrder where salesorder_id = '{}'".format(salesOrderId))


def insertSalesorder(tableCode, guestNo, staffId):
    time = common.tsToTime(common.getCurrentTs())

    salesorder_id = db_get("select max(salesorder_id) from SalesOrder")
    salesorder_id = 1 if salesorder_id[0][0] is None else salesorder_id[0][0] + 1

    query = "INSERT INTO [SalesOrder] ([salesorder_id], [salesorder_date], [expiry_date], [staff_id],[customer_id]," \
            "[transaction],[original_id],[custom],[comments],[subtotal],[discount],[rounding],[total_ex],[total_inc]," \
            "[status],[exported],[guest_no], customer_name) VALUES ({},'{}','{}', {}, 0,'DI',0,'{}','',0,0,0,0,0,0,0," \
            "{}, '{}')".format(
        salesorder_id, time, time, staffId, tableCode, guestNo, tableCode)

    db_put(query)

    return salesorder_id


# 更新salesorder价格
def updateSalesorderPrice(salesorderId):
    lines = db_get("select * from SalesOrderLine where salesorder_id = {}".format(salesorderId))
    if len(lines) == 0:
        return
    subtotal = 0
    total_ex = 0
    for line in lines:
        subtotal += line[10]
        total_ex += line[9]

    return db_put("update SalesOrder set subtotal={}, total_inc={}, total_ex={} where salesorder_id = {};".format(subtotal, subtotal, total_ex, salesorderId))


# no usage
def updateSalesorderGuestNo(salesorderId, guestNo):
    return db_put("update SalesOrder set guest_no = {} where salesorder_id = {};".format(guestNo, salesorderId))


def updateSalesorderTableCode(salesorderId, toTableCode):
    return db_put("update SalesOrder set custom = '{}' where salesorder_id = {};".format(toTableCode, salesorderId))


def getStockPrint(stockId):
    return db_get("select * from StockPrint where stock_id = {};".format(stockId))


def getCatPrint(catId):
    return db_get("select * from CatPrint where cat_id = {};".format(catId))


def getKeyboardPrint(kbId):
    return db_get("select * from KeyboardPrint where kb_id = {};".format(kbId))


def getSalesorderLineByLineId(lineId):
    return db_get("select * from SalesOrderLine where line_id = '{}';".format(lineId))


def getSalesorderLineByOrderlineId(orderlineId):
    return db_get("select * from SalesOrderLine where orderline_id = '{}';".format(orderlineId))


def goToKitchen(lineId, comments):
    # get stock Id from salesorderLine
    salesorderLine = getSalesorderLineByLineId(lineId)

    stockId = salesorderLine[0][2]
    salesorderId = salesorderLine[0][1]
    salesOrder = getSalesOrder(salesorderId)
    stock = getStockByStockId(stockId)
    catName = stock[0][13]
    catId = getCategoryId(catName)[0][0]
    staff = getStaffByStaffId(salesorderLine[0][17])
    if len(staff) > 0:
        staffName = staff[0][4] + staff[0][3]
    else:
        staffName = "online"

    printer = None

    # check keyboard print
    kbId = getKbIdFromKeyboardItem(stockId)
    # 如果不在keyboard item 里面， 就去keyboard 里面找
    if not kbId:
        kbId = getKbIdFromKeyboardCat(catId)

    # 如果找到了相应的kbId
    if kbId:
        kbId = kbId[0][0]
        keyboardPrint = getKeyboardPrint(kbId)
        if keyboardPrint:
            printer = keyboardPrint

    # check cat print
    catPrint = getCatPrint(catId)
    if catPrint:
        printer = catPrint

    # check stock print
    stockPrint = getStockPrint(stockId)
    if stockPrint:
        printer = stockPrint

    if printer:
        insertKitchen(printer, salesorderLine, salesOrder, stock, comments, staffName)
    else:
        raise Exception('Stock的printer没有正确配置. Stock id = {}'.format(stockId))


def insertKitchen(printers, salesorderLine, salesOrder, stock, comments, staffName):
    # salesorderLine is the original food
    # salesorderLines including the extra and taste, but all them need to go to kitchen
    query = ""
    orderline_id = salesorderLine[0][15]
    salesorderLines = getSalesorderLineByOrderlineId(orderline_id)

    for printer in printers:
        # hotFIX
        delivery_docket = printer[4]
        lineId = salesorderLine[0][0]
        orderline_id = salesorderLine[0][15]
        salesorderId = salesorderLine[0][1]
        tableCode = salesOrder[0][7]
        cat1 = stock[0][13]
        description = stock[0][11]
        description2 = stock[0][35]
        quantity = salesorderLine[0][11]
        orderTime = salesorderLine[0][18]
        cat2 = stock[0][14]
        printerName = printer[2]
        if delivery_docket:
            printerName = "+" + printerName
        comments = comments

        stockType = salesorderLine[0][12]

        for line in salesorderLines:
            lineId = line[0]
            stockType = line[12]

            stockId = line[2]
            stock = getStockByStockId(stockId)
            description = stock[0][11]
            description2 = stock[0][35]
            if stockType != 0: comments = ""

            query += "INSERT INTO Kitchen ([line_id], [orderline_id], [table_code], [staff_name],[cat1]," \
                     "[description],[description2],[unit],[quantity],[printer],[printer2],[order_time]," \
                     "[handwritting],[comments],[stock_type],[out_order],[customer_name],[cat2],[salesorder_id]," \
                     "[status],[original_line_id])VALUES('{}','{}','{}','{}','{}','{}','{}','1', {},'{}','{}','{}',0, " \
                     "'{}', {},'0','{}','{}', {},null,null);".format(lineId, orderline_id, tableCode, staffName,
                                                                     cat1, description, description2, quantity,
                                                                     printerName, printerName, orderTime, comments,
                                                                     stockType, tableCode, cat2, salesorderId)

    return db_put(query)


def getStaff():
    query = "select staff_id, barcode, inactive, surname, given_names from Staff;"
    return db_get(query)


def getStaffByStaffId(staffId):
    query = "select staff_id, barcode, inactive, surname, given_names from Staff where staff_id = {};".format(staffId)
    return db_get(query)


def dropTableAndCreateSalesorderLineOnline():
    query = ("SET ANSI_NULLS ON;SET QUOTED_IDENTIFIER ON;" +
             "IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SalesorderLineOnline]') "
             "AND type in (N'U'))" +
             "CREATE TABLE [dbo].[SalesorderLineOnline]( [pos_line_id] [int] NULL, [online_line_id] [int] NULL, "
             "[salesorder_id] [int] NULL ) ON [PRIMARY] ;")
    db_put(query)
