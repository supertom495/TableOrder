import flask
from utils import ServiceUtil, ResponseUtil, UtilValidate
from models import Keyboard, KeyboardCat, KeyboardItem, Category, Stock, TasteStock, ExtraStock
from database import storeName

menu_blueprint = flask.Blueprint(
    'menu',
    __name__,
    url_prefix='/api/v1/menu'
)


@menu_blueprint.route('/keyboard', methods=['GET'])
def getKeyboard():
    keyboardList = Keyboard.getAll()

    data = []
    for item in keyboardList:
        keyboard = {}
        keyboard["kbId"] = item.kb_id
        keyboard["kbName"] = item.kb_name
        keyboard["kbName2"] = item.kb_name2
        keyboard["online"] = 1 if item.kb_name2 == 'online' else 0

        data.append(keyboard)

    result = ServiceUtil.returnSuccess(data)

    return ResponseUtil.success(result)


@menu_blueprint.route('/keyboardcat', methods=['GET'])
def getKeyboardCat():
    kbId = flask.request.args.get('kbId')

    if UtilValidate.isNotEmpty(kbId):
        keyboard = Keyboard.getById(kbId)

        if UtilValidate.isEmpty(keyboard):
            return ResponseUtil.error(ServiceUtil.errorDataNotFound('No such keyboard'))

    kbCatList = KeyboardCat.getByKbId(kbId)

    data = []

    # fill category information
    for item in kbCatList:
        kbCat = {}
        category = Category.getByCatName(item.cat_name)
        kbCat["catName"] = item.cat_name
        if UtilValidate.isNotEmpty(category):
            kbCat["catName2"] = category.cat_name2
        else:
            kbCat["catName2"] = ""
        kbCat["catId"] = item.cat_id
        kbCat["kbId"] = item.kb_id
        kbCat["inactive"] = item.invisible
        data.append(kbCat)

    result = ServiceUtil.returnSuccess(data)

    return ResponseUtil.success(result)


@menu_blueprint.route('/keyboarditem', methods=['GET'])
def getKeyboardItem():
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
            displayStock["kbId"] = kbItem.kb_id
            displayStock["imageUrl"] = "https://pos-static.redpayments.com.au/{}/img/{}.jpg".format(storeName,
                                                                                                    kbItem.item_barcode)
            displayStock["inactive"] = stock.inactive
            displayStock["show_extra"] = stock.show_extra
            displayStock["show_taste"] = stock.show_taste
            displayStock["barcode"] = stock.barcode
            displayStock["catId"] = kbItem.cat_id
            displayStock["btnBackColor"] = kbItem.btn_backcolor
            displayStock["description"] = stock.description3
            displayStock["description2"] = stock.description4
            displayStock["longdesc"] = stock.longdesc
            displayStock["dateModified"] = UtilValidate.dateToTs(stock.date_modified)
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

            if extra:
                for item in extra:
                    extraId = item.extra_id
                    displayStock["extra"].append(extraId)

            stockList.append(displayStock)

            data["content"]["stock"] = stockList
            # data["content"]["extra"] = [v for v in cachedExtra.values()]
            # data["content"]["taste"] = [v for v in cachedTaste.values()]

    result = ServiceUtil.returnSuccess(data)

    return ResponseUtil.success(result)


@menu_blueprint.route('/option', methods=['GET'])
def getOption():
    option = flask.request.args.get('option')
    stockId = flask.request.args.get('stockId')

    optionList = []
    extra = []
    taste = []
    optionSet = {}

    if option == 'extra':
        if stockId:
            extra = ExtraStock.getByStockId(stockId)
        else:
            extra = ExtraStock.getAll()
    elif option == 'taste':
        if stockId:
            taste = TasteStock.getByStockId(stockId)
        else:
            taste = TasteStock.getAll()
    else:
        return ResponseUtil.error(ServiceUtil.errorInvalidParameter('wrong option'))

    if UtilValidate.isNotEmpty(extra):
        optionSet = {item.extra_id for item in extra}
    if UtilValidate.isNotEmpty(taste):
        optionSet = {item.taste_id for item in taste}

    for option in optionSet:
        optionDict = {}
        stock = Stock.getByStockId(option)
        optionDict["stockId"] = option
        # custom1 用于分类
        optionDict["custom1"] = stock.custom1
        optionDict["cat2"] = stock.cat2
        optionDict["barcode"] = stock.barcode
        optionDict["price"] = Stock.getPrice(stock, stock.sell)
        optionDict["description"] = stock.description
        optionDict["description2"] = stock.description2
        optionList.append(optionDict)

    result = ServiceUtil.returnSuccess(optionList)

    return ResponseUtil.success(result)



# def return_img_stream(img_local_path):
#   import base64
#   img_stream = ''
#   with open(img_local_path, 'rb') as img_f:
#     img_stream = img_f.read()
#     img_stream = base64.b64encode(img_stream)
#   return img_stream
#
# @menu_blueprint.route('/image', methods=['GET'])
# def index():
#     img = return_img_stream('./image/Image-1.jpeg')
#     return img