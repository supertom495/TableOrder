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


    for kbItem in kbItems:
        stock = Stock.getStockById(kbItem[1])[0]
        displayStock = {}
        displayStock["stockId"] = int(stock[0])
        displayStock["barcode"] = stock[1]
        displayStock["description"] = stock[2]
        displayStock["description2"] = stock[3]
        displayStock["price"] = float(round(stock[4]*Decimal(1.1), 2))
        displayStock["image"] = "https://pos-static.redpayments.com.au/{}/img/{}.jpg".format("bbqhot", stock[1])
        data[kbItem[0]]["stocks"].append(displayStock)

    ResponseUtil.success(result, [v for v in data.values()])
    return result


common.setVar()
app.run()