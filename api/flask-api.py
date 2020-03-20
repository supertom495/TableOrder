import flask
import common
import posOperation
from ServiceUtil import ServiceUtil
from ResponseUtil import ResponseUtil
import Keyboard
import KeyboardCat
import KeyboardItem
import Category
import Stock
from decimal import Decimal
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/table', methods=['GET'])
def getTable():
    res = ServiceUtil.returnSuccess()
    data = posOperation.getTable()
    ResponseUtil.success(res, data)
    return res

@app.route('/stock', methods=['GET'])
def getStock():
    # a = time.time()
    result = ServiceUtil.returnSuccess()
    # find activate keyboard id
    kbId = Keyboard.getActiveKeyboard()
    if len(kbId) == 0:
        return ResponseUtil.errorDataNotFound(result, "未找到激活的keyboard")
    kbId = kbId[0][0]

    # find activate category by keyboard id
    # this catId is using in keyboard only
    kbCat = KeyboardCat.getActiveKeyboardCat(kbId)
    if len(kbCat) == 0:
        return ResponseUtil.errorDataNotFound(result, "未找到激活的keyboard category")
    kbCatIds = [i[0] for i in kbCat]
    kbCatCodes = [i[1] for i in kbCat]

    # find relate keyboard Item by kbCatId and kbId
    kbItems = KeyboardItem.getAvtiveKeyboardItem(tuple(kbCatIds), kbId)
    if len(kbItems) == 0:
        return ResponseUtil.errorDataNotFound(result, "未找到激活的keyboard item")

    data = {}
    # fill category information
    for i in range(len(kbCatIds)):
        data[kbCatIds[i]] = {}
        catName = Category.getCategoryName(kbCatCodes[i])
        data[kbCatIds[i]]["catName"] = catName[0][0]
        data[kbCatIds[i]]["catName2"] = catName[0][1]
        data[kbCatIds[i]]["stocks"] = []

    taste = Stock.getStockTaste()
    extra = Stock.getStockExtra()

    # merge the same stock with different option
    sortedTaste = {k: [] for (k, v) in extra}
    for (k, v) in taste:
        if k in sortedTaste:
            sortedTaste[k].append(v)

    sortedExtra = {k: [] for (k, v) in extra}
    for (k, v) in extra:
        if k in sortedExtra:
            sortedExtra[k].append(v)

    cachedOption = {}

    for kbItem in kbItems:
        stock = Stock.getStockById(kbItem[1])[0]
        displayStock = {}
        displayStock["stockId"] = int(stock[0])
        displayStock["barcode"] = stock[1]
        displayStock["description"] = stock[2]
        displayStock["description2"] = stock[3]
        displayStock["price"] = float(round(stock[4]*Decimal(1.1), 2))
        displayStock["image"] = "https://pos-static.redpayments.com.au/{}/img/{}.jpg".format("bbqhot", stock[1])
        displayStock["taste"] = []
        displayStock["extra"] = []
        if stock[0] in sortedTaste:
            for tasteId in sortedTaste[stock[0]]:
                displayTaste = {}
                if tasteId in cachedOption:
                    displayTaste = cachedOption[tasteId]
                else:
                    stock = Stock.getStockById(tasteId)[0]
                    displayTaste["stockId"] = int(stock[0])
                    displayTaste["barcode"] = stock[1]
                    displayTaste["description"] = stock[2]
                    displayTaste["description2"] = stock[3]
                    cachedOption[tasteId] = displayTaste
                displayStock["taste"].append(displayTaste)

        if stock[0] in sortedExtra:
            for extraId in sortedExtra[stock[0]]:
                displayExtra = {}
                if extraId in cachedOption:
                    displayExtra = cachedOption[extraId]
                else:
                    stock = Stock.getStockById(extraId)[0]
                    displayExtra["stockId"] = int(stock[0])
                    displayExtra["barcode"] = stock[1]
                    displayExtra["description"] = stock[2]
                    displayExtra["description2"] = stock[3]
                    cachedOption[extraId] = displayExtra

                displayStock["extra"].append(displayExtra)


        data[kbItem[0]]["stocks"].append(displayStock)

    ResponseUtil.success(result, [v for v in data.values()])
    # b = time.time()
    # print(b - a)

    return result


common.setVar()
app.run()