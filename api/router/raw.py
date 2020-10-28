import time
import flask
from deprecated import deprecated
from models import Tables, KeyboardCat, KeyboardItem, Stock, Category, ExtraStock, TasteStock, Staff, Salesorder, \
    SalesorderLine, Site, Kitchen, GlobalSetting
from utils import ServiceUtil, ResponseUtil, UtilValidate
from database import flaskConfig
from service import SalesorderService, SalesorderLineService

raw_blueprint = flask.Blueprint(
    'raw',
    __name__,
    url_prefix=''
)


@raw_blueprint.route('/', methods=['GET'])
def home():
    return "<h1>RPOS online order</h1><h3>Store name: {}  V:1.32.0</h3><p>This site has API for self-ordering.</p>".format(
        flaskConfig.get('StoreName'))


@raw_blueprint.route('/stock', methods=['GET'])
def getStock():
    # find activate keyboard categories
    kbCat = KeyboardCat.getActivateKeyboardCat()

    if UtilValidate.isEmpty(kbCat):
        return ResponseUtil.error(ServiceUtil.errorDataNotFound("Please check if keyboard'kb_name2 is online"))

    kbId = kbCat[0].kb_id
    kbCatIds = [i.cat_id for i in kbCat]

    # find relate keyboard Item by kbCatId and kbId
    kbItems = KeyboardItem.getAvtiveKeyboardItem(tuple(kbCatIds), kbId)
    if len(kbItems) == 0:
        return ResponseUtil.error(ServiceUtil.errorDataNotFound("未找到激活的keyboard item"))

    stockMap = {}
    # fill category information
    for item in kbCat:
        stockMap[item.cat_id] = {}
        category = Category.getByCatName(item.cat_name)
        stockMap[item.cat_id]["catName"] = item.cat_name
        if UtilValidate.isNotEmpty(category):
            stockMap[item.cat_id]["catName2"] = category.cat_name2
        else:
            stockMap[item.cat_id]["catName2"] = ""

        stockMap[item.cat_id]["stocks"] = []

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

    # Get Menu rule
    sizeLevelOptionDisallowRules = GlobalSetting.getMenuSizeLevelOptionDisallow()
    menuOptionLimitationRules = GlobalSetting.getMenuOptionLimitation()

    for kbItem in kbItems:
        if not kbItem.item_barcode.strip(): continue
        stock = Stock.getByBarcode(kbItem.item_barcode)
        if UtilValidate.isEmpty(stock): continue

        displayStock = {}
        displayStock["stockId"] = int(stock.stock_id)
        displayStock["sizeLevelOptionDisallowRules"] = loadMenuSizeLevelOptionDisallowRules(stock.stock_id,
                                                                                            sizeLevelOptionDisallowRules)
        displayStock["menuOptionLimitationRules"] = loadMenuOptionLimitationRules(stock.stock_id,
                                                                                  menuOptionLimitationRules)
        displayStock["inactive"] = stock.inactive
        displayStock["show_extra"] = stock.show_extra
        displayStock["show_taste"] = stock.show_taste
        displayStock["barcode"] = stock.barcode
        displayStock["btnBackColor"] = kbItem.btn_backcolor
        displayStock["description"] = stock.description3
        displayStock["description2"] = stock.description4
        displayStock["longdesc"] = stock.longdesc
        displayStock["longdesc2"] = stock.longdesc2
        displayStock["taste"] = []
        displayStock["extra"] = []
        # put different size level price
        displayStock["price"] = {}
        displayStock["price"][0] = Stock.getPrice(stock, stock.sell)

        if UtilValidate.isNotEmpty(stock.custom1):
            displayStock["price"][1] = [Stock.getPrice(stock, stock.sell), stock.custom1]

        if UtilValidate.isNotEmpty(stock.custom2):
            displayStock["price"][2] = [Stock.getPrice(stock, stock.sell2), stock.custom2]

        if UtilValidate.isNotEmpty(stock.custom3):
            displayStock["price"][3] = [Stock.getPrice(stock, stock.sell3), stock.custom3]

        if UtilValidate.isNotEmpty(stock.custom4):
            displayStock["price"][4] = [Stock.getPrice(stock, stock.sell4), stock.custom4]

        if stock.stock_id in sortedExtra:
            for extraId in sortedExtra[stock.stock_id]:
                displayStock["extra"].append(extraId)
                if extraId not in cachedExtra:
                    displayExtra = {}
                    extraStock = Stock.getByStockId(extraId)
                    displayExtra["stockId"] = int(extraStock.stock_id)
                    displayExtra["inactive"] = extraStock.inactive
                    displayExtra["custom1"] = extraStock.custom1
                    displayExtra["cat2"] = extraStock.cat2
                    displayExtra["barcode"] = extraStock.barcode
                    displayExtra["price"] = Stock.getPrice(extraStock, extraStock.sell)
                    displayExtra["description"] = extraStock.description3
                    displayExtra["description2"] = extraStock.description4
                    cachedExtra[extraId] = displayExtra

        if stock.stock_id in sortedTaste:
            for tasteId in sortedTaste[stock.stock_id]:
                displayStock["taste"].append(tasteId)
                if tasteId not in cachedTaste:
                    displayTaste = {}
                    tasteStock = Stock.getByStockId(tasteId)
                    displayTaste["stockId"] = int(tasteStock.stock_id)
                    displayTaste["inactive"] = tasteStock.inactive
                    displayTaste["custom1"] = tasteStock.custom1
                    displayTaste["cat2"] = tasteStock.cat2
                    displayTaste["barcode"] = tasteStock.barcode
                    displayTaste["price"] = Stock.getPrice(tasteStock, tasteStock.sell)
                    displayTaste["description"] = tasteStock.description3
                    displayTaste["description2"] = tasteStock.description4
                    cachedTaste[tasteId] = displayTaste



        displayStock["extra"].sort()
        displayStock["taste"].sort()
        stockMap[kbItem.cat_id]["stocks"].append(displayStock)

    data = {}
    data["stock"] = [v for v in stockMap.values()]
    data["extra"] = [cachedExtra[v] for v in sorted(cachedExtra)]
    data["taste"] = [cachedTaste[v] for v in sorted(cachedTaste)]

    # image url
    data["imageUrl"] = UtilValidate.getImageUrl(flask.request.host)

    result = ServiceUtil.returnSuccess(data)

    return ResponseUtil.success(result)


@raw_blueprint.route('/stafftoken', methods=['PUT'])
def getStaffToken():
    # result = ServiceUtil.returnSuccess()

    barcode = flask.request.form.get('barcode')
    staff = Staff.getStaffByBarcode(barcode)
    if staff == None:
        return ResponseUtil.error(ServiceUtil.errorDataNotFound("no such a staff"))

    toBeEncrypted = barcode + str(int(time.time()) + 3600)

    cipherText = UtilValidate.encryption(toBeEncrypted).decode('UTF-8')

    result = ServiceUtil.returnSuccess(cipherText)
    return ResponseUtil.success(result)


@raw_blueprint.route('/salesorder', methods=['POST'])
def apiNewSalesorder():
    token = flask.request.form.get('token')
    tableCode = flask.request.form.get('tableCode')
    guestNo = flask.request.form.get('guestNo')

    result = SalesorderService.newSalesorder({"token": token, "tableCode": tableCode, "guestNo": guestNo})

    if result["code"] != "0":
        return ResponseUtil.error(result)

    return ResponseUtil.success(result)


@raw_blueprint.route('/salesorder', methods=['PUT'])
def resetTable():
    result = ServiceUtil.returnSuccess()
    tableCode = flask.request.form.get('tableCode')
    # salesorderId = flask.request.form.get('salesorderId')
    table = Tables.getTableByTableCode(tableCode)
    salesorder = Salesorder.getSalesorderByTableCode(tableCode)
    table.staff_id = 0
    table.table_status = 0
    salesorder.status = 11
    result = ServiceUtil.returnSuccess({"status": "salesoder {} closed".format(salesorder.salesorder_id)})
    return ResponseUtil.success(result)


@deprecated()
@raw_blueprint.route('/salesorderline', methods=['POST'])
def apiInsertSalesorderLine():
    token = flask.request.form.get('token')
    tableCode = flask.request.form.get('tableCode')
    salesorderId = flask.request.form.get('salesorderId')
    salesorderLines = flask.request.form.get('salesorderLines')

    result = SalesorderLineService.insertSalesorderLine({"token": token, "tableCode": tableCode,
                                                         "salesorderId": salesorderId,
                                                         "salesorderLines": salesorderLines,
                                                         "goToKitchen": True})
    if result["code"] != "0":
        return ResponseUtil.error(result)

    return ResponseUtil.success(result)


@raw_blueprint.route('/salesorder', methods=['GET'])
def getSalesorder():
    # result = ServiceUtil.returnSuccess()
    tableCode = flask.request.args.get('tableCode')
    if tableCode is None:
        return ResponseUtil.error(ServiceUtil.errorMissingParameter())
    table = Tables.getTableByTableCode(tableCode)

    # test if table exists
    if UtilValidate.isEmpty(table):
        return ResponseUtil.success(ServiceUtil.errorDataNotFound('Wrong table code'))

    # test if table is closed
    if table.table_status == 0:
        return ResponseUtil.success(ServiceUtil.errorWrongLogic('Inactive table'))

    # find the Salesorder
    salesorder = Salesorder.getSalesorderByTableCode(tableCode)
    if UtilValidate.isEmpty(salesorder):
        return ResponseUtil.error(ServiceUtil.errorWrongLogic('No order found', code=3001))

    # do not return invalid salesorder (when status is 10, 11)
    if salesorder.status == 10 or salesorder.status == 11:
        return ResponseUtil.error(ServiceUtil.errorWrongLogic('No order found', code=3001))

    # put Salesorder lines to data
    data = {}
    data["salesorderId"] = salesorder.salesorder_id
    data["startTime"] = salesorder.salesorder_date
    data["guestNo"] = salesorder.guest_no
    data["imageUrl"] = UtilValidate.getImageUrl(flask.request.host)
    data["total"] = float(salesorder.total_inc)
    data["salesorderLines"] = {}

    salesorderLines = SalesorderLine.getBySalesorderId(salesorder.salesorder_id)

    for line in salesorderLines:
        stock = Stock.getByStockId(line.stock_id)
        quantity = line.quantity
        newItem = fullfillStockMap(stock, quantity)
        newItem["price"] = float(round(line.print_inc, 2))

        if line.parentline_id == 0:
            newItem["timeOrdered"] = line.time_ordered
            kitchenLine = Kitchen.getByLineId(line.line_id)
            newItem["comments"] = kitchenLine.comments if kitchenLine else ""
            newItem["option"] = []
            newItem["other"] = []
            if line.size_level == 0: newItem["custom"] = ""
            if line.size_level == 1: newItem["custom"] = stock.custom1
            if line.size_level == 2: newItem["custom"] = stock.custom2
            if line.size_level == 3: newItem["custom"] = stock.custom3
            if line.size_level == 4: newItem["custom"] = stock.custom4

            data["salesorderLines"][line.line_id] = newItem
        else:
            orderline = data["salesorderLines"].get(line.orderline_id)
            if orderline:
                if line.parentline_id == 1 or line.parentline_id == 2:
                    orderline["option"].append(newItem)
                else:
                    orderline["option"].append(newItem)

    data["salesorderLines"] = [v for v in data["salesorderLines"].values()]

    result = ServiceUtil.returnSuccess(data)

    return ResponseUtil.success(result)


@raw_blueprint.route('/testing', methods=['GET'])
def testing():
    items = KeyboardItem.getAllById(2)
    for item in items:
        # find keyboard item
        keyboardItem = KeyboardItem.getByBarcodeAndKbId(item.item_barcode, 2)
        if UtilValidate.isEmpty(keyboardItem):
            raise Exception('keyboardItem does not have matched item. (NO item_barcode matched)')
    return 'ok'


@raw_blueprint.route('/testing2', methods=['GET'])
def testing2():
    raise Exception('testing exc')


# TODO delete this method, this is for test only
@raw_blueprint.route('/salesorderById', methods=['GET'])
def getSalesorderById():
    # result = ServiceUtil.returnSuccess()
    salesorderId = flask.request.args.get('salesorderId')

    # find the Salesorder
    salesorder = Salesorder.getSalesorderById(salesorderId)
    if UtilValidate.isEmpty(salesorder):
        return ResponseUtil.error(ServiceUtil.errorWrongLogic('No order found', code=3001))

    # put Salesorder lines to data
    data = {}
    data["salesorderId"] = salesorder.salesorder_id
    data["startTime"] = salesorder.salesorder_date
    data["guestNo"] = salesorder.guest_no
    data["imageUrl"] = UtilValidate.getImageUrl(flask.request.host)
    data["total"] = float(salesorder.total_inc)
    data["salesorderLines"] = {}

    salesorderLines = SalesorderLine.getBySalesorderId(salesorder.salesorder_id)

    for line in salesorderLines:
        stock = Stock.getByStockId(line.stock_id)
        quantity = line.quantity
        newItem = fullfillStockMap(stock, quantity)
        newItem["price"] = float(round(line.print_inc, 2))

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
            if line.parentline_id == 1 or line.parentline_id == 2:
                data["salesorderLines"][line.orderline_id]['option'].append(newItem)
            else:
                data["salesorderLines"][line.orderline_id]['other'].append(newItem)

    data["salesorderLines"] = [v for v in data['salesorderLines'].values()]

    result = ServiceUtil.returnSuccess(data)

    return ResponseUtil.success(result)


@raw_blueprint.route('/table', methods=['GET'])
def getTable():
    # result = ServiceUtil.returnSuccess()
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

    result = ServiceUtil.returnSuccess(data)

    return ResponseUtil.success(result)


@raw_blueprint.route('/favicon.ico')
def favicon():
    return ""


@raw_blueprint.route('/table', methods=['PUT'])
def swapTable():
    #

    fromTableCode = flask.request.form.get('fromTableCode')
    toTableCode = flask.request.form.get('toTableCode')
    token = flask.request.form.get('token')

    if token is None or toTableCode is None or toTableCode is None:
        return ResponseUtil.error(ServiceUtil.errorMissingParameter())

    tokenValid, staffId = UtilValidate.tokenValidation(token)
    if not tokenValid:
        return ResponseUtil.error(ServiceUtil.errorSecurityNotLogin('Invalid token'))

    fromTable = Tables.getTableByTableCode(fromTableCode)
    toTable = Tables.getTableByTableCode(toTableCode)

    # test if table exists
    if UtilValidate.isEmpty(fromTable) or UtilValidate.isEmpty(toTable):
        return ResponseUtil.error(ServiceUtil.errorDataNotFound('Wrong table code'))

    # test if table occupied by POS
    if fromTable.staff_id != 0 and fromTable.staff_id is not None \
            and toTable.staff_id != 0 and toTable.staff_id is not None:
        return ResponseUtil.error(ServiceUtil.errorWrongLogic('Table is using by POS'))

    # only approve the table have people to table without people
    if fromTable.table_status == 0 or toTable.table_status != 0:
        return ResponseUtil.error(
            ServiceUtil.errorWrongLogic('Not allowed, only approve the occupied table to vacant table',
                                        code=3001))

    fromSalesorder = Salesorder.getSalesorderByTableCode(fromTable.table_code)
    if UtilValidate.isEmpty(fromSalesorder) or fromSalesorder.status == 11:
        return ResponseUtil.error(ServiceUtil.errorDataAccess('Order is paid or not exist'))

    # swap the table contents
    tempTableStatus = fromTable.table_status
    tempTableStartTime = fromTable.start_time
    fromTable.table_status = toTable.table_status
    fromTable.start_time = toTable.start_time
    toTable.table_status = tempTableStatus
    toTable.start_time = tempTableStartTime

    # update the given salesorder to given tableCode
    fromSalesorder.custom = toTable.table_code

    result = ServiceUtil.returnSuccess()
    return ResponseUtil.success(result)


def fullfillStockMap(stock: Stock, quantity: int) -> dict:
    stockMap = {}
    stockMap["barcode"] = stock.barcode
    stockMap["description"] = stock.description
    stockMap["description2"] = stock.description2
    # stockMap["price"] = Stock.getStockPrice(stock, stock.sell)
    stockMap["stockId"] = int(stock.stock_id)
    stockMap["quantity"] = quantity

    return stockMap


def loadMenuSizeLevelOptionDisallowRules(stockId, rules):
    results = []
    for rule in rules:
        ruleDetails = rule.setting_value.split(';')
        if ruleDetails[0] == '' or ruleDetails[0] == str(stockId):
            results.append(rule.setting_value.split(';', 1)[1])

    return results


def loadMenuOptionLimitationRules(stockId, rules):
    results = []
    for rule in rules:
        ruleDetails = rule.setting_value.split(';')
        if ruleDetails[0] == '' or ruleDetails[0] == str(stockId):
            results.append(rule.setting_value.split(';', 1)[1])
    return results
