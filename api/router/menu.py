import flask
from utils import ServiceUtil, ResponseUtil, UtilValidate
from models import Keyboard, KeyboardCat, KeyboardItem, Category

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

    kbId = flask.request.args.get('kbId')

    keyboard = Keyboard.getById(kbId)

    if UtilValidate.isEmpty(keyboard):
        return ResponseUtil.errorDataNotFound(result, 'No such keyboard')

    kbCatList = KeyboardCat.getByKbId(kbId)

    data = []

    kbCatIds = [i.cat_id for i in kbCatList]
    kbCatCodes = [i.cat_code for i in kbCatList]

    # fill category information
    for item in kbCatList:
        kbCat = {}
        category = Category.getByCatCode(item.cat_code)
        if UtilValidate.isNotEmpty(category):
            kbCat["catName"] = category.cat_name
            kbCat["catName2"] = category.cat_name2
            kbCat["catId"] = category.cat_id
            kbCat["inactive"] = category.inactive
            data.append(kbCat)

    ResponseUtil.success(result, data)

    return result


@menu_blueprint.route('/keyboarditem', methods=['GET'])
def getKeyboardItem():
    result = ServiceUtil.returnSuccess()

    kbId = flask.request.args.get('kbId')
    catId = flask.request.args.get('catId')
    page = flask.request.args.get('page')
    size = flask.request.args.get('size')

    keyboard = Keyboard.getById(kbId)

    res = KeyboardItem.getByCatIdAndKbId(1, 2)

    ResponseUtil.success(result)

    return result