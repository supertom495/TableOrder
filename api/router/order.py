import flask
from utils import ServiceUtil, ResponseUtil, UtilValidate
from models import Staff
from database import init_db, db_session, storeName
import time, json
from service import SalesorderService, SalesorderLineService, PaymentService, DocketService, DocketLineService


order_blueprint = flask.Blueprint(
    'order',
    __name__,
    url_prefix='/api/v1/order'
)

@order_blueprint.route('/salesorderprepay', methods=['POST'])
def apiNewPrepaidSalesorder():
    """
    create a order with option of paid or unpaid, go to kitchen or not
    if paid, need to specify the amount paid, how it is paid
    if go to kitchen, then write it to kitchen
    """
    token = flask.request.form.get('token')
    tableCode = flask.request.form.get('tableCode')
    guestNo = flask.request.form.get('guestNo') or 0
    salesorderLines = flask.request.form.get('salesorderLines')
    isPaid = flask.request.form.get('isPaid')
    gotoKitchen = flask.request.form.get('gotoKitchen')
    paymentDetail = flask.request.form.get('paymentDetail')
    freeId = flask.request.form.get('freeId')

    result = ServiceUtil.returnSuccess()

    if UtilValidate.isEmpty(isPaid):
        return ResponseUtil.errorMissingParameter(result, "isPaid")

    if UtilValidate.isEmpty(gotoKitchen):
        return ResponseUtil.errorMissingParameter(result, "gotoKitchen")

    # is this order paid
    if isPaid.lower() in ['true', 'false']:
        isPaid = isPaid.lower() == 'true'
    else:
        return ResponseUtil.errorInvalidParameter(result, "isPaid")

    # should this order go to kitchen
    if gotoKitchen.lower() in ['true', 'false']:
        gotoKitchen = gotoKitchen.lower() == 'true'
    else:
        return ResponseUtil.errorInvalidParameter(result, "gotoKitchen")

    # if it is paid, does it include payment detail
    if isPaid:
        if UtilValidate.isEmpty(paymentDetail):
            ResponseUtil.errorMissingParameter(result, "paymentDetail")


    # if table code then dine in else takeaway
    result = SalesorderService.newSalesorder({"token":token, "tableCode":tableCode, "guestNo":guestNo,
                                              "isPaid":isPaid})

    if result['code'] != '0':
        return result

    tableCode = result.get("data").get("tableCode")

    # go to kitchen
    salesorderId = result.get('data')['salesorderId']
    result = SalesorderLineService.insertSalesorderLine({"token":token, "tableCode":tableCode,
                                                        "salesorderId":salesorderId, "salesorderLines":salesorderLines,
                                                        "goToKitchen":gotoKitchen, "freeId": freeId})
    if result['code'] != '0':
        return result

    ResponseUtil.success(result, {"salesorderId": salesorderId, "tableCode":tableCode})


    if isPaid:

        paymentDetail = json.loads(paymentDetail)

        subtotal = 0
        for payment in paymentDetail:
            subtotal += float(payment["amount"])

        # insert into docket
        docketResult = DocketService.newDocket({"token":token, "tableCode":tableCode,
                                                        "subtotal":subtotal, "guestNo":guestNo})
        if docketResult['code'] != '0':
            return docketResult

        docketId = docketResult['data']['docketId']

        # insert into docket line
        DocketLineService.insertDocketLine({"docketId": docketId, "salesorderId": salesorderId})

        # insert into payments
        PaymentService.insertPayment({"docketId": docketId, "paymentDetail": paymentDetail})

    return result


@order_blueprint.route('/salesordertrial', methods=['POST'])
def calculateSalesorderTotal():

    token = flask.request.form.get('token')
    salesorderLines = flask.request.form.get('salesorderLines')

    result = SalesorderLineService.calculateSalesorderLine({"token":token, "salesorderLines":salesorderLines})


    return result