import flask
from utils import ServiceUtil, ResponseUtil, UtilValidate
from models import Staff
from database import init_db, db_session, storeName
import time
from service import salesorderService, salesorderLineService


order_blueprint = flask.Blueprint(
    'order',
    __name__,
    url_prefix='/api/v1/order'
)

@order_blueprint.route('/salesorderprepay', methods=['POST'])
def apiNewPrepaidSalesorder():

    token = flask.request.form.get('token')
    tableCode = flask.request.form.get('tableCode')
    guestNo = flask.request.form.get('guestNo') or 0
    salesorderLines = flask.request.form.get('salesorderLines')
    isPaid = flask.request.form.get('isPaid')
    gotoKitchen = flask.request.form.get('gotoKitchen')

    if (UtilValidate.isNotEmpty(isPaid)):
        if isPaid.lower() == 'true':
            isPaid = True
        else:
            isPaid = False
    else:
        isPaid = False

    if (UtilValidate.isNotEmpty(gotoKitchen)):
        if gotoKitchen.lower() == 'true':
            gotoKitchen = True
        else:
            gotoKitchen = False
    else:
        gotoKitchen = False

    # if table code then dine in else takeaway
    result = salesorderService.newSalesorder({"token":token, "tableCode":tableCode, "guestNo":guestNo,
                                              "isPaid":isPaid})

    if result['code'] != '0':
        return result

    tableCode = result.get("data").get("tableCode")

    # go to kitchen
    salesorderId = result.get('data')['salesorderId']
    result = salesorderLineService.insertSalesorderLine({"token":token, "tableCode":tableCode,
                                                        "salesorderId":salesorderId, "salesorderLines":salesorderLines,
                                                        "goToKitchen":gotoKitchen})
    if result['code'] != '0':
        return result

    ResponseUtil.success(result, {"salesorderId": salesorderId, "tableCode":tableCode})

    return result


@order_blueprint.route('/salesordertrial', methods=['POST'])
def calculateSalesorderTotal():

    token = flask.request.form.get('token')
    salesorderLines = flask.request.form.get('salesorderLines')

    result = salesorderLineService.calculateSalesorderLine({"token":token, "salesorderLines":salesorderLines})


    return result