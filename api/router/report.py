import flask
from utils import ServiceUtil, ResponseUtil, UtilValidate
from models import Keyboard, Docket, Payment, Tables, DocketLine, Stock
from decimal import Decimal
from datetime import datetime
from database import init_db, db_session, storeName

report_blueprint = flask.Blueprint(
    'report',
    __name__,
    url_prefix='/api/v1/report'
)

@report_blueprint.route('/report', methods=['GET'])
def getReport():

    date = flask.request.args.get('date')

    try:
        docketList = Docket.getAll(date)
    except:
        return ResponseUtil.error(ServiceUtil.errorInvalidParameter("bad date"))

    if UtilValidate.isEmpty(docketList):
        return ResponseUtil.success(ServiceUtil.returnSuccess("no data"))


    data = {}
    data['summary'] = {}
    data['summary']['guest'] = 0
    data['summary']['totalInc'] = 0
    data['summary']['totalEx'] = 0
    data['summary']['takeAwayInc'] = 0
    data['summary']['takeAwayEx'] = 0
    data['summary']['dineInInc'] = 0
    data['summary']['dineInEx'] = 0

    for item in docketList:
        data['summary']['guest'] += item.guest_no
        data['summary']['totalInc'] += item.total_inc
        data['summary']['totalEx'] += item.total_ex

        if item.custom[0:2] == 'TA':
            data['summary']['takeAwayInc'] += item.total_inc
            data['summary']['takeAwayEx'] += item.total_ex
        else:
            data['summary']['dineInInc'] += item.total_inc
            data['summary']['dineInEx'] += item.total_ex


    # -----------Payment-----------
    try:
        paymentList = Payment.getAll(date)
    except:
        return ResponseUtil.error(ServiceUtil.errorInvalidParameter("bad date"))

    data["payment"] = {}

    for item in paymentList:
        if item.paymenttype not in data["payment"]:
            data["payment"][item.paymenttype] = 0

        data["payment"][item.paymenttype] += item.amount


    # -----------Table-----------
    try:
        tableList = Tables.getTableAll()
    except:
        return ResponseUtil.error(ServiceUtil.errorInvalidParameter("bad table"))

    data["table"] = {}

    data["table"]['totalNumberOfTable'] = len(tableList)
    data['table']['totalNumberOfCovers'] = len(docketList)

    data['table']['takeAway'] = 0
    data['table']['coversBefore5'] = 0
    data['table']['coversAfter5'] = 0
    data['table']['averageCheckPerPerson'] = round(float(data['summary']['totalInc']/data['summary']['guest']), 2)
    data['table']['averageCoverPerTable'] = round(float(data['table']['totalNumberOfCovers']/data["table"]['totalNumberOfTable']), 2)


    for item in docketList:
        if item.custom[0:2] == 'TA':
            data['table']['takeAway'] += 1

        if item.docket_date < datetime.strptime(date + ' 17:00:00', '%Y%m%d %H:%M:%S'):
            data['table']['coversBefore5'] += 1
        else:
            data['table']['coversAfter5'] += 1

    data['table']['averageCheckPerTakeAway'] = 0 if data['table']['takeAway']==0 else round(float(data['summary']['takeAwayInc']/data['table']['takeAway']), 2)

    # -----------discount-----------

    docketIds = [i.docket_id for i in docketList]

    docketLineList = DocketLine.getByDocketId(tuple(docketIds))
    discounts = []

    data['discount'] = discounts

    for line in docketLineList:
        discountDetail = {}
        if line.rrp != line.sell_inc:
            discountDetail['originalPrice'] = float(line.rrp)
            discountDetail['discountPrice'] = float(line.sell_inc)
            discountDetail['discountPercentage'] = round(1 - float(line.sell_inc/line.rrp), 2)
            discountDetail['discountProduct'] = Stock.getByStockId(line.stock_id).description
            discountDetail['discountQuantity'] = line.quantity
            discountDetail['discountTableCode'] = Docket.getByDocketId(line.docket_id).custom
            discountDetail['discountDatetime'] = Docket.getByDocketId(line.docket_id).docket_date

            discounts.append(discountDetail)

    # -----------parse-----------

    for key in data['summary']:
        if type(data['summary'][key]) is Decimal:
            data['summary'][key] = float(data['summary'][key])

    for key in data["payment"]:
        if type(data["payment"][key]) is Decimal:
            data["payment"][key] = float(data["payment"][key])

    result = ServiceUtil.returnSuccess(data)

    return ResponseUtil.success(result)