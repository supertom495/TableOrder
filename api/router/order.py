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


    if UtilValidate.isEmpty(isPaid):
        return ResponseUtil.error(ServiceUtil.errorMissingParameter("isPaid"))

    if UtilValidate.isEmpty(gotoKitchen):
        return ResponseUtil.error(ServiceUtil.errorMissingParameter("gotoKitchen"))

    # is this order paid
    if isPaid.lower() in ['true', 'false']:
        isPaid = isPaid.lower() == 'true'
    else:
        return ResponseUtil.error(ServiceUtil.errorInvalidParameter("isPaid"))

    # should this order go to kitchen
    if gotoKitchen.lower() in ['true', 'false']:
        gotoKitchen = gotoKitchen.lower() == 'true'
    else:
        return ResponseUtil.error(ServiceUtil.errorInvalidParameter("gotoKitchen"))

    # if it is paid, does it include payment detail
    if isPaid:
        if UtilValidate.isEmpty(paymentDetail):
            return ResponseUtil.error(ServiceUtil.errorMissingParameter("paymentDetail"))

    # if table code then dine in else takeaway
    result = SalesorderService.newSalesorder({"token":token, "tableCode":tableCode, "guestNo":guestNo,
                                              "isPaid":isPaid})

    if result["code"] != "0":
        return ResponseUtil.error(result)

    tableCode = result.get("data").get("tableCode")

    # go to kitchen
    salesorderId = result.get('data')['salesorderId']
    result = SalesorderLineService.insertSalesorderLine({"token":token, "tableCode":tableCode,
                                                        "salesorderId":salesorderId, "salesorderLines":salesorderLines,
                                                        "goToKitchen":gotoKitchen})
    if result["code"] != "0":
        return ResponseUtil.error(result)


    if isPaid:

        paymentDetail = json.loads(paymentDetail)

        subtotal = 0
        for payment in paymentDetail:
            subtotal += float(payment["amount"])

        # insert into docket
        docketResult = DocketService.newDocket({"token":token, "tableCode":tableCode,
                                                        "subtotal":subtotal, "guestNo":guestNo})
        if docketResult["code"] != "0":
            return ResponseUtil.error(docketResult)


        docketId = docketResult['data']['docketId']

        # insert into docket line
        docketLineResult = DocketLineService.insertDocketLine({"docketId": docketId, "salesorderId": salesorderId})

        if docketLineResult["code"] != "0":
            return ResponseUtil.error(docketLineResult)


        # insert into payments
        paymentResult = PaymentService.insertPayment({"docketId": docketId, "paymentDetail": paymentDetail})

        if paymentResult["code"] != "0":
            return ResponseUtil.error(paymentResult)


    result = ServiceUtil.returnSuccess({"salesorderId": salesorderId, "tableCode":tableCode})

    return ResponseUtil.success(result)


@order_blueprint.route('/salesordertrial', methods=['POST'])
def calculateSalesorderTotal():

    token = flask.request.form.get('token')
    salesorderLines = flask.request.form.get('salesorderLines')

    result = SalesorderLineService.calculateSalesorderLine({"token":token, "salesorderLines":salesorderLines})

    if result["code"] != "0":
        return ResponseUtil.error(result)

    return ResponseUtil.success(result)