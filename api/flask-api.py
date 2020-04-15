import flask
from flask_cors import *
from utils import ServiceUtil, ResponseUtil, UtilValidate
from database import init_db, db_session, storeName
from models import Tables, Keyboard, KeyboardCat, KeyboardItem, Stock, Category, ExtraStock, TasteStock, Staff, Salesorder, SalesorderLine, Site
from service import salesorderService, salesorderLineService
import time

app = flask.Flask(__name__)
CORS(app, supports_credentials=True, resource=r'/*')
app.config["DEBUG"] = True


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.before_request
def logTime():
    app.logger.info("START: "+ str(time.time()))


@app.after_request
def commit_session(response):
    db_session.commit()
    app.logger.info('RESPONSE - %s', response.data)
    app.logger.info("END  : "+ str(time.time()))
    return response


@app.route('/', methods=['GET'])
def home():
    return "<h1>RPOS online order</h1><p>This site has API for self-ordering.</p>"


@app.route('/stock', methods=['GET'])
def getStock():

    result = ServiceUtil.returnSuccess()

    # find activate keyboard categories
    kbCat = KeyboardCat.getActivateKeyboardCat()

    if UtilValidate.isEmpty(kbCat):
        return ResponseUtil.errorDataNotFound(result, "Please check if keyboard'kb_name2 is online or keyboard cat has cat code")

    kbId = kbCat[0].kb_id
    kbCatIds = [i.cat_id for i in kbCat]
    kbCatCodes = [i.cat_code for i in kbCat]

    # find relate keyboard Item by kbCatId and kbId
    kbItems = KeyboardItem.getAvtiveKeyboardItem(tuple(kbCatIds), kbId)
    if len(kbItems) == 0:
        return ResponseUtil.errorDataNotFound(result, "未找到激活的keyboard item")

    stockMap = {}
    # fill category information
    for i in range(len(kbCatIds)):
        stockMap[kbCatIds[i]] = {}
        category = Category.getByCatCode(kbCatCodes[i])
        stockMap[kbCatIds[i]]["catName"] = category.cat_name
        stockMap[kbCatIds[i]]["catName2"] = category.cat_name2
        stockMap[kbCatIds[i]]["stocks"] = []

    taste = TasteStock.getAll()
    extra = ExtraStock.getAll()

    # merge the same stock with different option
    sortedTaste = {item.stock_id: [] for item in taste}
    for item in taste:
        if item.stock_id in sortedTaste:
            sortedTaste[item.stock_id].append(item.taste_id)

    sortedExtra = {item.stock_id: [] for item in extra}
    for item in extra:
        if item.stock_id in sortedExtra:
            sortedExtra[item.stock_id].append(item.extra_id)

    cachedExtra = {}
    cachedTaste = {}

    for kbItem in kbItems:
        if not kbItem.item_barcode.strip(): continue
        stock = Stock.getStockByBarcode(kbItem.item_barcode)

        displayStock = {}
        displayStock["stockId"] = int(stock.stock_id)
        displayStock["inactive"] = stock.inactive
        displayStock["show_extra"] = stock.show_extra
        displayStock["show_taste"] = stock.show_taste
        displayStock["barcode"] = stock.barcode
        displayStock["btnBackColor"] = kbItem.btn_backcolor
        displayStock["description"] = stock.description
        displayStock["description2"] = stock.description2
        displayStock["taste"] = []
        displayStock["extra"] = []
        # put different size level price
        displayStock["price"] = {}
        displayStock["price"][0] = Stock.getStockPrice(stock, stock.sell)

        if UtilValidate.isNotEmpty(stock.custom1):
            displayStock["price"][1] = [Stock.getStockPrice(stock, stock.sell), stock.custom1]

        if UtilValidate.isNotEmpty(stock.custom2):
            displayStock["price"][2] = [Stock.getStockPrice(stock, stock.sell2), stock.custom2]

        if UtilValidate.isNotEmpty(stock.custom3):
            displayStock["price"][3] = [Stock.getStockPrice(stock, stock.sell3), stock.custom3]

        if UtilValidate.isNotEmpty(stock.custom4):
            displayStock["price"][4] = [Stock.getStockPrice(stock, stock.sell4), stock.custom4]

        if stock.stock_id in sortedTaste:
            for tasteId in sortedTaste[stock.stock_id]:
                displayStock["taste"].append(tasteId)
                if tasteId not in cachedTaste:
                    displayTaste = {}
                    stock = Stock.getStockById(tasteId)
                    displayTaste["stockId"] = int(stock.stock_id)
                    displayTaste["custom1"] = stock.custom1
                    displayTaste["barcode"] = stock.barcode
                    displayTaste["price"] = Stock.getStockPrice(stock, stock.sell)
                    displayTaste["description"] = stock.description
                    displayTaste["description2"] = stock.description2
                    cachedTaste[tasteId] = displayTaste

        if stock.stock_id in sortedExtra:
            for extraId in sortedExtra[stock.stock_id]:
                displayStock["extra"].append(extraId)
                if extraId not in cachedExtra:
                    displayExtra = {}
                    stock = Stock.getStockById(extraId)
                    displayExtra["stockId"] = int(stock.stock_id)
                    displayExtra["custom1"] = stock.custom1
                    displayExtra["barcode"] = stock.barcode
                    displayExtra["price"] = Stock.getStockPrice(stock, stock.sell)
                    displayExtra["description"] = stock.description
                    displayExtra["description2"] = stock.description2
                    cachedExtra[extraId] = displayExtra

        stockMap[kbItem.cat_id]["stocks"].append(displayStock)

    data = {}
    data["stock"] = [v for v in stockMap.values()]
    data["extra"] = [v for v in cachedExtra.values()]
    data["taste"] = [v for v in cachedTaste.values()]
    data["imageUrl"] = "https://pos-static.redpayments.com.au/{}/img/".format(storeName)

    ResponseUtil.success(result, data)

    return result



@app.route('/stafftoken', methods=['PUT'])
def getStaffToken():
    result = ServiceUtil.returnSuccess()

    barcode = flask.request.form.get('barcode')
    staff = Staff.getStaffByBarcode(barcode)
    if staff == None:
        return ResponseUtil.errorDataNotFound(result, "no such a staff")

    toBeEncrypted = barcode+str(int(time.time())+3600)
    app.logger.info('Before encryption:%s', toBeEncrypted)

    cipherText = UtilValidate.encryption(toBeEncrypted).decode('UTF-8')
    ResponseUtil.success(result, cipherText)
    return result


@app.route('/salesorder', methods=['POST'])
def apiNewSalesorder():

    token = flask.request.form.get('token')
    tableCode = flask.request.form.get('tableCode')
    guestNo = flask.request.form.get('guestNo')

    result = salesorderService.newSalesorder({"token":token, "tableCode":tableCode, "guestNo":guestNo})

    return result


@app.route('/salesorder-prepay', methods=['POST'])
def apiNewPrepaidSalesorder():

    token = flask.request.form.get('token')
    tableCode = flask.request.form.get('tableCode')
    guestNo = flask.request.form.get('guestNo') or 0
    salesorderLines = flask.request.form.get('salesorderLines')
    isPaid = flask.request.form.get('isPaid')

    if (UtilValidate.isNotEmpty(isPaid)):
        if isPaid.lower() == 'true':
            isPaid = True
        else:

            isPaid = False
    else:
        isPaid = False

    app.logger.info(token)
    app.logger.info(tableCode)
    app.logger.info(guestNo)
    app.logger.info(salesorderLines)
    app.logger.info(isPaid)


    # if table code then dine in else takeaway
    result = salesorderService.newSalesorder({"token":token, "tableCode":tableCode, "guestNo":guestNo,
                                              "isPaid":isPaid})

    if result['code'] != '0':
        return result
    # if paid then go to kitchen else not
    salesorderId = result.get('data')['salesorderId']
    result = salesorderLineService.insertSalesorderLine({"token":token, "tableCode":tableCode,
                                                        "salesorderId":salesorderId, "salesorderLines":salesorderLines,
                                                        "goToKitchen":isPaid})

    ResponseUtil.success(result, {"salesorderId": salesorderId})

    return result


# TODO delete this method, this is for test only
@app.route('/salesorder', methods=['PUT'])
def resetTable():
    result = ServiceUtil.returnSuccess()
    tableCode = flask.request.form.get('tableCode')
    # salesorderId = flask.request.form.get('salesorderId')
    table = Tables.getTableByTableCode(tableCode)
    salesorder = Salesorder.getSalesorderByTableCode(tableCode)
    table.staff_id = 0
    table.table_status = 0
    salesorder.status = 11
    ResponseUtil.success(result, "salesoder {} closed".format(salesorder.salesorder_id))
    return result


@app.route('/salesorderline', methods=['POST'])
def apiInsertSalesorderLine():

    token = flask.request.form.get('token')
    tableCode = flask.request.form.get('tableCode')
    salesorderId = flask.request.form.get('salesorderId')
    salesorderLines = flask.request.form.get('salesorderLines')

    app.logger.info(token)
    app.logger.info(tableCode)
    app.logger.info(salesorderId)
    app.logger.info(salesorderLines)

    result = salesorderLineService.insertSalesorderLine({"token":token, "tableCode":tableCode,
                                                     "salesorderId":salesorderId, "salesorderLines":salesorderLines,
                                                     "goToKitchen":True})

    return result

@app.route('/salesorder', methods=['GET'])
def getSalesorder():
    result = ServiceUtil.returnSuccess()
    tableCode = flask.request.args.get('tableCode')
    if tableCode is None:
        return  ResponseUtil.errorMissingParameter(result)
    table = Tables.getTableByTableCode(tableCode)

    # test if table exists
    if UtilValidate.isEmpty(table):
        return ResponseUtil.errorDataNotFound(result, 'Wrong table code')

    # test if table is closed
    if table.table_status == 0:
        return ResponseUtil.errorWrongLogic(result, 'Inactive table')

    # find the Salesorder
    salesorder = Salesorder.getSalesorderByTableCode(tableCode)
    if UtilValidate.isEmpty(salesorder):
        return ResponseUtil.errorWrongLogic(result, 'No order found', code=3001)

    # do not return invalid salesorder (when status is 10, 11)
    if salesorder.status == 10 or salesorder.status == 11:
        return ResponseUtil.errorWrongLogic(result, 'No order found', code=3001)

    # put Salesorder lines to data
    data = {}
    data["salesorderId"] = salesorder.salesorder_id
    data["startTime"] = salesorder.salesorder_date
    data["guestNo"] = salesorder.guest_no
    data["imageUrl"] = "https://pos-static.redpayments.com.au/bbqhot/img/"
    data["total"] = float(salesorder.total_inc)
    data["salesorderLines"] = {}

    salesorderLines = SalesorderLine.getBySalesorderId(salesorder.salesorder_id)

    for line in salesorderLines:
        stock = Stock.getStockById(line.stock_id)
        quantity = line.quantity
        newItem = fullfillStockMap(stock, quantity)
        newItem["price"] = float(round(line.print_inc,2))

        if line.parentline_id == 0:
            newItem["timeOrdered"] = line.time_ordered
            newItem["comments"] = ''
            newItem["option"] = []
            newItem["other"] = []
            if line.size_level == 0: newItem["custom"] = ""
            if line.size_level == 1: newItem["custom"] = stock.custom1
            if line.size_level == 2: newItem["custom"] = stock.custom2
            if line.size_level == 3: newItem["custom"] = stock.custom3
            if line.size_level == 4: newItem["custom"] = stock.custom4

            data["salesorderLines"][line.line_id] = newItem
        else:
            if line.parentline_id  == 1 or line.parentline_id == 2:
                data["salesorderLines"][line.orderline_id]["option"].append(newItem)
            else:
                data["salesorderLines"][line.orderline_id]["other"].append(newItem)

    data["salesorderLines"] = [v for v in data["salesorderLines"].values()]


    ResponseUtil.success(result, data)

    return result


# TODO delete this method, this is for test only
@app.route('/salesorderById', methods=['GET'])
def getSalesorderById():
    result = ServiceUtil.returnSuccess()
    salesorderId = flask.request.args.get('salesorderId')

    # find the Salesorder
    salesorder = Salesorder.getSalesorderById(salesorderId)
    if UtilValidate.isEmpty(salesorder):
        return ResponseUtil.errorWrongLogic(result, 'No order found', code=3001)

    # put Salesorder lines to data
    data = {}
    data["salesorderId"] = salesorder.salesorder_id
    data["startTime"] = salesorder.salesorder_date
    data["guestNo"] = salesorder.guest_no
    data["imageUrl"] = "https://pos-static.redpayments.com.au/bbqhot/img/"
    data["total"] = float(salesorder.total_inc)
    data["salesorderLines"] = {}

    salesorderLines = SalesorderLine.getBySalesorderId(salesorder.salesorder_id)

    for line in salesorderLines:
        stock = Stock.getStockById(line.stock_id)
        quantity = line.quantity
        newItem = fullfillStockMap(stock, quantity)
        newItem["price"] = float(round(line.print_inc,2))

        if line.parentline_id == 0:
            newItem["timeOrdered"] = line.time_ordered
            newItem["comments"] = ''
            newItem["option"] = []
            newItem["other"] = []
            if line.size_level == 0: newItem["custom"] = ""
            if line.size_level == 1: newItem["custom"] = stock.custom1
            if line.size_level == 2: newItem["custom"] = stock.custom2
            if line.size_level == 3: newItem["custom"] = stock.custom3
            if line.size_level == 4: newItem["custom"] = stock.custom4

            data["salesorderLines"][line.line_id] = newItem
        else:
            if line.parentline_id  == 1 or line.parentline_id == 2:
                data["salesorderLines"][line.orderline_id]["option"].append(newItem)
            else:
                data["salesorderLines"][line.orderline_id]["other"].append(newItem)

    data["salesorderLines"] = [v for v in data["salesorderLines"].values()]


    ResponseUtil.success(result, data)

    return result


@app.route('/table', methods=['GET'])
def getTable():
    result = ServiceUtil.returnSuccess()
    tables = Tables.getTableAll()
    data = {}
    data["tables"] = []
    for table in tables:
        mappedTable = {}
        mappedTable["tableId"] = table.table_id
        mappedTable["tableStatus"] = table.table_status
        mappedTable["siteId"] = table.site_id
        mappedTable["startTime"] = table.start_time
        mappedTable["inactive"] = table.inactive
        mappedTable["tableCode"] = table.table_code
        mappedTable["seats"] = table.seats
        mappedTable["guestNo"] = 0

        # find the number of guest
        if table.table_status != 0:
            salesorder = Salesorder.getSalesorderByTableCode(table.table_code)
            if UtilValidate.isNotEmpty(salesorder):
                mappedTable["guestNo"] = salesorder.guest_no

        data["tables"].append(mappedTable)

    sites = Site.getSiteAll()
    data["sites"] = []
    for site in sites:
        mappedSite = {}
        mappedSite["siteName"] = site.site_name
        mappedSite["siteName2"] = site.site_name2
        mappedSite["siteId"] = site.site_id
        mappedSite["inactive"] = site.inactive
        data["sites"].append(mappedSite)

    ResponseUtil.success(result, data)

    return result


@app.route('/table', methods=['PUT'])
def swapTable():
    result = ServiceUtil.returnSuccess()

    fromTableCode = flask.request.form.get('fromTableCode')
    toTableCode = flask.request.form.get('toTableCode')
    token = flask.request.form.get('token')


    if token is None or toTableCode is None or toTableCode is None:
        return ResponseUtil.errorMissingParameter(result)


    tokenValid, staffId = UtilValidate.tokenValidation(token)
    if not tokenValid:
        return ResponseUtil.errorSecurityNotLogin(result, 'Invalid token')


    fromTable = Tables.getTableByTableCode(fromTableCode)
    toTable = Tables.getTableByTableCode(toTableCode)

    # test if table exists
    if UtilValidate.isEmpty(fromTable) or UtilValidate.isEmpty(toTable):
        return ResponseUtil.errorDataNotFound(result, 'Wrong table code')


    # test if table occupied by POS
    if fromTable.staff_id != 0 and fromTable.staff_id is not None\
            and toTable.staff_id != 0 and toTable.staff_id is not None:
        return ResponseUtil.errorWrongLogic(result, 'Table is using by POS')


    # only approve the table have people to table without people
    if fromTable.table_status == 0 or toTable.table_status != 0:
        return ResponseUtil.errorWrongLogic(result, 'Not allowed, only approve the occupied table to vacant table', code=3001)


    fromSalesorder = Salesorder.getSalesorderByTableCode(fromTable.table_code)
    if UtilValidate.isEmpty(fromSalesorder) or fromSalesorder.status == 11:
        return ResponseUtil.errorDataAccess(result, 'Order is paid or not exist')

    # swap the table contents
    tempTableStatus = fromTable.table_status
    tempTableStartTime =  fromTable.start_time
    fromTable.table_status = toTable.table_status
    fromTable.start_time = toTable.start_time
    toTable.table_status = tempTableStatus
    toTable.start_time = tempTableStartTime

    # update the given salesorder to given tableCode
    fromSalesorder.custom = toTable.table_code

    return result


def fullfillStockMap(stock:Stock, quantity:int) -> dict:
    stockMap = {}
    stockMap["barcode"] = stock.barcode
    stockMap["description"] = stock.description
    stockMap["description2"] = stock.description2
    # stockMap["price"] = Stock.getStockPrice(stock, stock.sell)
    stockMap["stockId"] = int(stock.stock_id)
    stockMap["quantity"] = quantity

    return stockMap

if __name__ == '__main__':
    init_db()
    app.debug = True
    app.run(port=5001)
