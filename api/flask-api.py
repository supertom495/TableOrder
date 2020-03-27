import flask
from flask_cors import *
import common
from utils import ServiceUtil, ResponseUtil, UtilValidate
from database import init_db, db_session
from sqlalchemy.ext.declarative import DeclarativeMeta
from models import Tables, Keyboard, KeyboardCat, KeyboardItem, Stock, Category, ExtraStock, TasteStock, Staff, Salesorder, SalesorderLine
import decimal, datetime, json, time

app = flask.Flask(__name__)
CORS(app, supports_credentials=True, resource=r'/*')
app.config["DEBUG"] = True


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.after_request
def commit_session(response):
    db_session.commit()
    return response

@app.route('/', methods=['GET'])
def home():
    # from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
    # try:
    #     result = session.query(profile.name).filter(...).one()
    #     print
    #     result
    # except NoResultFound:
    #     print
    #     'No result was found'
    # except MultipleResultsFound:
    #     print
    #     'Multiple results were found'
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"



def alchemyEncoder():
    _visited_objs = []
    class AlchemyEncoder(json.JSONEncoder):
        def jsonify(self, obj):
            """JSON encoder function for SQLAlchemy special classes."""
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            elif isinstance(obj, decimal.Decimal):
                return float(obj)

        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)
                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    fields[field] = self.jsonify(obj.__getattribute__(field))
                # a json-encodable dict
                return fields
            return json.JSONEncoder.default(self, obj)
    return AlchemyEncoder



@app.route('/table', methods=['GET'])
def getTable():

    u = Tables.query.all()

    return json.dumps(u, cls=alchemyEncoder(), check_circular=True)


@app.route('/stock', methods=['GET'])
def getStock():

    a = time.time()

    result = ServiceUtil.returnSuccess()

    # find activate keyboard categories
    kbCat = KeyboardCat.getActivateKeyboardCat()
    if UtilValidate.isEmpty(kbCat):
        return ResponseUtil.errorDataNotFound(result, "keyboard或keyboard categories 未正确配置")

    kbId = kbCat[0].kb_id
    kbCatIds = [i.cat_id for i in kbCat]
    kbCatCodes = [i.cat_code for i in kbCat]

    # find relate keyboard Item by kbCatId and kbId
    kbItems = KeyboardItem.getAvtiveKeyboardItem(tuple(kbCatIds), kbId)
    if len(kbItems) == 0:
        return ResponseUtil.errorDataNotFound(result, "未找到激活的keyboard item")

    data = {}
    # fill category information
    for i in range(len(kbCatIds)):
        data[kbCatIds[i]] = {}
        catName = Category.getCategoryNameByCatCode(kbCatCodes[i])
        data[kbCatIds[i]]["catName"] = catName.cat_name
        data[kbCatIds[i]]["catName2"] = catName.cat_name2
        data[kbCatIds[i]]["stocks"] = []

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

    cachedOption = {}

    for kbItem in kbItems:
        stock = Stock.getStockById(kbItem.stock_id)
        displayStock = {}
        displayStock["stockId"] = int(stock.stock_id)
        displayStock["barcode"] = stock.barcode
        displayStock["description"] = stock.description
        displayStock["description2"] = stock.description2
        displayStock["price"] = float(round(stock.sell*decimal.Decimal(1.1), 2))
        displayStock["image"] = "https://pos-static.redpayments.com.au/{}/img/{}.jpg".format("bbqhot", stock.barcode)
        displayStock["taste"] = []
        displayStock["extra"] = []
        if stock.stock_id in sortedTaste:
            for tasteId in sortedTaste[stock.stock_id]:
                displayTaste = {}
                if tasteId in cachedOption:
                    displayTaste = cachedOption[tasteId]
                else:
                    stock = Stock.getStockById(tasteId)
                    displayTaste["stockId"] = int(stock.stock_id)
                    displayTaste["barcode"] = stock.barcode
                    displayTaste["description"] = stock.description
                    displayTaste["description2"] = stock.description2
                    cachedOption[tasteId] = displayTaste
                displayStock["taste"].append(displayTaste)

        if stock.stock_id in sortedExtra:
            for extraId in sortedExtra[stock.stock_id]:
                displayExtra = {}
                if extraId in cachedOption:
                    displayExtra = cachedOption[extraId]
                else:
                    stock = Stock.getStockById(extraId)
                    displayExtra["stockId"] = int(stock.stock_id)
                    displayExtra["barcode"] = stock.barcode
                    displayExtra["description"] = stock.description
                    displayExtra["description2"] = stock.description2
                    cachedOption[extraId] = displayExtra

                displayStock["extra"].append(displayExtra)

        data[kbItem.cat_id]["stocks"].append(displayStock)

    ResponseUtil.success(result, [v for v in data.values()])
    b = time.time()
    print(b - a)

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

    # timestamp = toBeEncrypted[-10:]
    # print(timestamp)
    cipherText = UtilValidate.encryption(toBeEncrypted).decode('UTF-8')
    # app.logger.info('After encryption:%s', cipherText)
    # b = UtilValidate.decryption(cipherText).decode("UTF-8")
    # print("decode===", b)
    ResponseUtil.success(result, cipherText)
    return result


@app.route('/salesorder', methods=['POST'])
def newSalesorder():
    result = ServiceUtil.returnSuccess()

    token = flask.request.form.get('token')
    tableCode = flask.request.form.get('tableCode')
    guestNo = flask.request.form.get('guestNo')

    if token is None or tableCode is None or guestNo is None:
        return  ResponseUtil.errorMissingParameter(result)

    # verifying token
    tokenValid, staffId = UtilValidate.tokenValidation(token)
    if not tokenValid:
        return ResponseUtil.errorSecurityNotLogin(result, 'Invalid token')

    table = Tables.getTableByTableCode(tableCode)

    # test if table exists
    if UtilValidate.isEmpty(table):
        return ResponseUtil.errorDataNotFound(result, 'Wrong table code')

    # test if table occupied by POS
    if table.staff_id == 0 or table.staff_id == None:
        return ResponseUtil.errorWrongLogic(result, 'Fail to open table, table is using by POS')

    # test if table is already opened
    if table.table_status != 0:
        return ResponseUtil.errorWrongLogic(result, 'Fail to open table, table is already opened', code=3001)

    # Activate Table
    Tables.activateTable(tableCode, UtilValidate.tsToTime(UtilValidate.getCurrentTs()))
    # insert a new salesorder
    salesorderId = Salesorder.insertSalesorder(tableCode, guestNo, staffId, UtilValidate.tsToTime(UtilValidate.getCurrentTs()))

    ResponseUtil.success(result, {"salesorderId" : salesorderId})

    return result


@app.route('/salesorderline', methods=['POST'])
def insertSalesorderLine():
    result = ServiceUtil.returnSuccess()

    token = flask.request.form.get('token')
    tableCode = flask.request.form.get('tableCode')         # TODO VALIDATE TABLECODE
    salesorderId = flask.request.form.get('salesorderId')   # TODO VALIDATE SALESORDERID
    salesorderLines = flask.request.form.get('salesorderLines')

    if token is None or tableCode is None or salesorderId is None or salesorderLines is None:
        return  ResponseUtil.errorMissingParameter(result)

    tokenValid, staffId = UtilValidate.tokenValidation(token)
    if not tokenValid:
        return ResponseUtil.errorSecurityNotLogin(result, 'Invalid token')


    # test if table occupied by POS
    tableOccupation = Tables.getTableOccupation(tableCode) # FIXME
    if UtilValidate.isEmpty(tableOccupation):
        return ResponseUtil.errorWrongLogic(result, 'Fail to open table, table is using by POS')


    salesorderLines = json.loads(salesorderLines)
    print(salesorderLines)
    for stockId, options in salesorderLines.items():
        if len(options) != 5:
            return ResponseUtil.errorWrongLogic(result, 'content incorrect')

        stock = Stock.getStockById(stockId)
        sizeLevel = options["sizeLevel"]
        quantity = options["quantity"]
        price = stock.sell
        if sizeLevel == 0 or sizeLevel == 1:
            price = stock.sell
        if sizeLevel == 2:
            price = stock.sell2
        if sizeLevel == 3:
            price = stock.sell3
        if sizeLevel == 4:
            price = stock.sell4

        parentlineId = 0
        originalSalesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, stockId, sizeLevel, price, quantity, staffId, UtilValidate.tsToTime(UtilValidate.getCurrentTs()), parentlineId)

        # def insertSalesorderLine(cls, salesorderId, stockId, sizeLevel, price, quantity, parentlineId, orderlineId,
        #                          staffId, time):

        for extra in options["extra"]:
            parentlineId = 2
            sizeLevel = 0
            price = 0 # FIXME IT HAS PRICE
            quantity = 1
            salesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, extra, sizeLevel, price, quantity, staffId, UtilValidate.tsToTime(UtilValidate.getCurrentTs()), parentlineId, orderlineId = originalSalesorderLineId)

        for taste in options["taste"]:
            parentlineId = 1
            sizeLevel = 0
            price = 0 # FIXME IT HAS PRICE
            quantity = 1
            salesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, taste, sizeLevel, price, quantity, staffId, UtilValidate.tsToTime(UtilValidate.getCurrentTs()), parentlineId, orderlineId = originalSalesorderLineId)

        comments = options["comments"]

        print(stockId, options)
    # for item in salesorderLines:
    #     result = posOperation.insertSalesorderLine(item, salesorderId, data["staffId"])
    #
    #     comments = item["comments"] or ""
    #     print("DISH: \n" +
    #           "salesorderId, line_id, last_line_id\n {} added\n".format(
    #               result))  # from the dish_line_id -> option_line_id
    #
    #     # find printer and insert into kitchen
    #     posOperation.goToKitchen(result[1], comments)
    #
    # posOperation.updateSalesorderPrice(salesorderId)

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
        return ResponseUtil.errorWrongLogic(result, 'No order found')

    # do not return invalid salesorder (when status is 10, 11)
    if salesorder.status == 10 or salesorder.status == 11:
        return ResponseUtil.errorWrongLogic(result, 'No order found')

    # put Salesorder lines to data
    data = {}
    data["salesorderId"] = salesorder.salesorder_id
    data["imageUrl"] = "https://pos-static.redpayments.com.au/bbqhot/img/"
    data["total"] = float(salesorder.total_inc)
    data["salesorderLines"] = []

    salesorderLines = SalesorderLine.getSalesorderLine(salesorder.salesorder_id)

    for i in range(len(salesorderLines)):
        if salesorderLines[i].parentline_id == 0:
            stock = Stock.getStockById(salesorderLines[i].stock_id)
            quantity = salesorderLines[i].quantity
            newItem = fullfillStockMap(stock, quantity)
            newItem["comments"] = ''
            newItem["extra"] = []
            newItem["taste"] = []
            # if there is next line
            if i+1 < len(salesorderLines):
                # test if is extra or taste then put in the dict
                if salesorderLines[i + 1].parentline_id == 1:
                    i += 1
                    stock = Stock.getStockById(salesorderLines[i].stock_id)
                    newTaste = fullfillStockMap(stock, quantity)
                    newItem["taste"].append(newTaste)
                elif salesorderLines[i + 1].parentline_id == 2:
                    i += 1
                    stock = Stock.getStockById(salesorderLines[i].stock_id)
                    newExtra = fullfillStockMap(stock, quantity)
                    newItem["extra"].append(newExtra)

            data["salesorderLines"].append(newItem)

    ResponseUtil.success(result, data)

    return result


def fullfillStockMap(stock:Stock, quantity:int) -> dict:
    stockMap = {}
    stockMap["barcode"] = stock.barcode
    stockMap["description"] = stock.description
    stockMap["description2"] = stock.description2
    stockMap["price"] = float(round(stock.sell * decimal.Decimal(1.1), 2))
    stockMap["stockId"] = int(stock.stock_id)
    stockMap["quantity"] = quantity

    return stockMap

if __name__ == '__main__':
    init_db()
    app.debug = True
    app.run(port=5001)
