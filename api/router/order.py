import flask
from utils import ServiceUtil, ResponseUtil, UtilValidate
from models import Tables, Docket, DocketOnline, RecordedDate
from database import db_session, flaskConfig
import json
from service import SalesorderService, SalesorderLineService, PaymentService, DocketService, DocketLineService, \
    SalesorderOnline, Salesorder, SalesorderLine, SalesorderLineOnline
import requests

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
    remark = flask.request.form.get('remark')
    actualId = flask.request.form.get('actualId')
    memberBarcode = flask.request.form.get('memberBarcode')

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
    result = SalesorderService.newSalesorder({"token": token, "tableCode": tableCode, "guestNo": guestNo,
                                              "isPaid": isPaid, "remark": remark, "actualId": actualId})

    if result["code"] != "0":
        return ResponseUtil.error(result)

    tableCode = result.get("data").get("tableCode")

    # go to kitchen
    salesorderId = result.get('data')['salesorderId']
    result = SalesorderLineService.insertSalesorderLine({"token": token, "tableCode": tableCode,
                                                         "salesorderId": salesorderId,
                                                         "salesorderLines": salesorderLines,
                                                         "goToKitchen": gotoKitchen, "actualId": actualId})
    if result["code"] != "0":
        return ResponseUtil.error(result)

    if isPaid:

        paymentDetail = json.loads(paymentDetail)

        subtotal = 0
        for payment in paymentDetail:
            subtotal += float(payment["amount"])

        # insert into docket
        docketResult = DocketService.newDocket({"token": token, "tableCode": tableCode,
                                                "subtotal": subtotal, "guestNo": guestNo, "remark": remark,
                                                "actualId": actualId, "memberBarcode": memberBarcode})
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

        # shut the table down
        Tables.deactivateTable(tableCode)

    result = ServiceUtil.returnSuccess({"salesorderId": salesorderId, "tableCode": tableCode})

    return ResponseUtil.success(result)


@order_blueprint.route('/salesorderline', methods=['POST'])
def apiInsertSalesorderLine():
    token = flask.request.form.get('token')
    tableCode = flask.request.form.get('tableCode')
    salesorderId = flask.request.form.get('salesorderId')
    salesorderLines = flask.request.form.get('salesorderLines')
    gotoKitchen = flask.request.form.get('gotoKitchen')
    actualId = flask.request.form.get('actualId')

    if UtilValidate.isEmpty(gotoKitchen):
        return ResponseUtil.error(ServiceUtil.errorMissingParameter("gotoKitchen"))

    # should this order go to kitchen
    if gotoKitchen.lower() in ['true', 'false']:
        gotoKitchen = gotoKitchen.lower() == 'true'
    else:
        return ResponseUtil.error(ServiceUtil.errorInvalidParameter("gotoKitchen"))

    result = SalesorderLineService.insertSalesorderLine({"token": token,
                                                         "tableCode": tableCode,
                                                         "salesorderId": salesorderId,
                                                         "salesorderLines": salesorderLines,
                                                         "goToKitchen": gotoKitchen,
                                                         "actualId": actualId})
    if result["code"] != "0":
        return ResponseUtil.error(result)

    return ResponseUtil.success(result)


@order_blueprint.route('/salesordertrial', methods=['POST'])
def calculateSalesorderTotal():
    token = flask.request.form.get('token')
    salesorderLines = flask.request.form.get('salesorderLines')

    result = SalesorderLineService.calculateSalesorderLine({"token": token, "salesorderLines": salesorderLines})

    if result["code"] != "0":
        return ResponseUtil.error(result)

    return ResponseUtil.success(result)


@order_blueprint.route('/docket', methods=['DELETE'])
def scanDeletedDocket():
    """用于已经付款的订单删除"""
    nowTime = UtilValidate.tsToTime(UtilValidate.getCurrentTs())
    recordedDate = RecordedDate.get(1)
    dockets = Docket.getByDate(recordedDate.date_modified)
    for docket in dockets:
        if docket.subtotal < 0:
            # 检查该单是否在记录单中
            refundDocketId = docket.original_id
            refundDocket = DocketOnline.getByDocketId(refundDocketId)
            if UtilValidate.isNotEmpty(refundDocket):
                response = cancelOrderRequest(refundDocket.docket_id, refundDocket.actual_id)
                # 如果取消失败 直接返回结果
                # 不更新记录时间
                if response.status_code != 200:
                    return response

    RecordedDate.update(1, nowTime)

    db_session.commit()
    return ResponseUtil.success()


@order_blueprint.route('/salesorder', methods=['DELETE'])
def scanDeletedSalesorder():
    """用于没有付款的订单删除"""
    activeOrders = SalesorderOnline.getActivateOrder()
    for order in activeOrders:
        salesorderId = order.salesorder_id
        salesorder = Salesorder.getSalesorderById(salesorderId)
        if UtilValidate.isEmpty(salesorder):
            response = cancelOrderRequest(order.salesorder_id, order.actual_id)
            if response.status_code == 200:
                order.status = -1
            print(response.text)
        else:
            if salesorder.status == 11:
                order.status = 11
            else:
                scanDeletedSalesorderLine(salesorderId, order.actual_id)

    db_session.commit()
    return ResponseUtil.success()


def scanDeletedSalesorderLine(salesorderId, actualId):
    """用于没有付款的订单菜品删除"""

    # 只检查 main dish
    salesorderLinesOnline = SalesorderLineOnline.getBySalesorderId(salesorderId)

    for lineOnline in salesorderLinesOnline:
        if lineOnline.status != -1:
            salesorderLine = SalesorderLine.get(lineOnline.line_id)
            if UtilValidate.isEmpty(salesorderLine):
                refundGoods = {
                    'stockId': lineOnline.stock_id,
                    'actualLineId': lineOnline.actual_line_id,
                    'quantity': lineOnline.quantity,
                }
                response = cancelDishRequest(lineOnline.salesorder_id, actualId, refundGoods)
                if response.status_code == 200:
                    lineOnline.status = -1
                print(response.text)


def cancelDishRequest(salesorderId, actualId, refundGoods):
    PiselUrl = flaskConfig.get('PiselUrl')
    url = '{}/api/pos/au/notify/order/goods_change'.format(PiselUrl)

    form = {
        "salesorderId": salesorderId,
        "relatedOrderNo": actualId,
        "refund_goods": json.dumps(refundGoods)
    }
    form = UtilValidate.addSign(form)

    print(form)
    response = requests.post(url, data=form)

    return response


def cancelOrderRequest(salesorderId, actualId):
    PiselUrl = flaskConfig.get('PiselUrl')
    url = '{}/api/pos/au/notify/order/cancel'.format(PiselUrl)

    form = {
        "salesorderId": salesorderId,
        "relatedOrderNo": actualId
    }

    form = UtilValidate.addSign(form)

    print(form)
    response = requests.post(url, data=form)

    return response
