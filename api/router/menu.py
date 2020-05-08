import flask
from utils import ServiceUtil, ResponseUtil, UtilValidate
from models import Keyboard, KeyboardCat, KeyboardItem, Category, Stock, TasteStock, ExtraStock
from database import init_db, db_session, storeName

menu_blueprint = flask.Blueprint(
    'menu',
    __name__,
    url_prefix='/api/v1/menu'
)

@menu_blueprint.route('/keyboard', methods=['GET'])
def getKeyboard():
    result = ServiceUtil.returnSuccess()

    keyboardList = Keyboard.getAll()

    data = []
    for item in keyboardList:
        keyboard = {}
        keyboard["kbId"] = item.kb_id
        keyboard["kbName"] = item.kb_name
        keyboard["kbName2"] = item.kb_name2

        data.append(keyboard)

    ResponseUtil.success(result, data)

    return result

@menu_blueprint.route('/keyboardcat', methods=['GET'])
def getKeyboardCat():
    result = ServiceUtil.returnSuccess()

    kbId = f
    lask.request.args.get('kbId')

    keyboard = Keyboard.getById(kbId)

    if UtilValidate.isEmpty(keyboard):
        return ResponseUtil.errorDataNotFound(result, 'No such keyboard')

    kbCatList = KeyboardCat.getByKbId(kbId)

    data = []

    # kbCatIds = [i.cat_id for i in kbCatList]
    # kbCatCodes = [i.cat_code for i in kbCatList]

    # fill category information
    for item in kbCatList:
        kbCat = {}
        category = Category.getByCatCode(item.cat_code)
        if UtilValidate.isNotEmpty(category):
            kbCat["catName"] = category.cat_name
            kbCat["catName2"] = category.cat_name2
            kbCat["catId"] = item.cat_id
            kbCat["inactive"] = category.inactive
            data.append(kbCat)

    ResponseUtil.success(result, data)

    return result


@menu_blueprint.route('/keyboarditem', methods=['GET'])
def getKeyboardItem():
    result = ServiceUtil.returnSuccess()

    kbId = flask.request.args.get('kbId')
    catId = flask.request.args.get('catId')
    page = flask.request.args.get('page', type=int)
    pageSize = flask.request.args.get('pageSize', type=int)

    page = page if page else 1
    pageSize = pageSize if pageSize else 10

    # find relate keyboard Item by kbId and catId
    pagedkbItems = KeyboardItem.getByCatIdAndKbIdPagination(kbId, catId, page, pageSize)

    data = {}
    data["hasNext"] = pagedkbItems.has_next
    data["hasPrevious"] = pagedkbItems.has_previous
    data["totalElements"] = pagedkbItems.total
    data["totalPages"] = pagedkbItems.pages
    data["page"] = page
    data["pageSize"] = pageSize
    data["content"] = {}

    kbItems = pagedkbItems.items

    if len(kbItems) != 0:
        stockList = []

        cachedExtra = {}
        cachedTaste = {}

        for kbItem in kbItems:
            if not kbItem.item_barcode.strip(): continue
            stock = Stock.getByBarcode(kbItem.item_barcode)
            if UtilValidate.isEmpty(stock): continue

            taste = TasteStock.getByStockId(stock.stock_id)
            extra = ExtraStock.getByStockId(stock.stock_id)

            displayStock = {}
            displayStock["stockId"] = int(stock.stock_id)
            displayStock["inactive"] = stock.inactive
            displayStock["show_extra"] = stock.show_extra
            displayStock["show_taste"] = stock.show_taste
            displayStock["barcode"] = stock.barcode
            displayStock["btnBackColor"] = kbItem.btn_backcolor
            displayStock["description"] = stock.description
            displayStock["description2"] = stock.description2
            displayStock["longdesc"] = stock.longdesc
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

            if taste:
                for item in taste:
                    tasteId = item.taste_id
                    displayStock["taste"].append(tasteId)
                    if tasteId not in cachedTaste:
                        displayTaste = {}
                        stock = Stock.getByStockId(tasteId)
                        displayTaste["stockId"] = int(stock.stock_id)
                        displayTaste["custom1"] = stock.custom1
                        displayTaste["cat2"] = stock.cat2
                        displayTaste["barcode"] = stock.barcode
                        displayTaste["price"] = Stock.getPrice(stock, stock.sell)
                        displayTaste["description"] = stock.description
                        displayTaste["description2"] = stock.description2
                        cachedTaste[tasteId] = displayTaste

            if extra:
                for item in extra:
                    extraId = item.extra_id
                    displayStock["extra"].append(extraId)
                    if extraId not in cachedExtra:
                        displayExtra = {}
                        stock = Stock.getByStockId(extraId)
                        displayExtra["stockId"] = int(stock.stock_id)
                        displayExtra["custom1"] = stock.custom1
                        displayExtra["cat2"] = stock.cat2
                        displayExtra["barcode"] = stock.barcode
                        displayExtra["price"] = Stock.getPrice(stock, stock.sell)
                        displayExtra["description"] = stock.description
                        displayExtra["description2"] = stock.description2
                        cachedExtra[extraId] = displayExtra

            stockList.append(displayStock)

            data["content"]["stock"] = stockList
            data["content"]["extra"] = [v for v in cachedExtra.values()]
            data["content"]["taste"] = [v for v in cachedTaste.values()]
            data["content"]["imageUrl"] = "https://pos-static.redpayments.com.au/{}/img/".format(storeName)

    ResponseUtil.success(result, data)

    return result