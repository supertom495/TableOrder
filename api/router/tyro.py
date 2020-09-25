import json
import flask
from utils import ServiceUtil, ResponseUtil, UtilValidate
from models import Tables, Staff, Salesorder

tyro_blueprint = flask.Blueprint(
    'tyro',
    __name__,
    url_prefix='/api/v1/tyro'
)


@tyro_blueprint.route('/diagnostic', methods=['GET'])
def diagnostic():
    data = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'

    return ResponseUtil.tyro_success(data)


@tyro_blueprint.route('/open-sales', methods=['GET'])
def getOpenSales():
    operatorId = flask.request.args.get('operatorId')
    mid = flask.request.args.get('mid')
    tid = flask.request.args.get('tid')
    table = flask.request.args.get('table')

    tableCode = table
    barcode = operatorId

    if tableCode is None:
        return ResponseUtil.error(ServiceUtil.errorMissingParameter(), 400)
    table = Tables.getTableByTableCode(tableCode)

    # if table does not exists
    if UtilValidate.isEmpty(table):
        return ResponseUtil.error(ServiceUtil.errorDataNotFound('Wrong table code'), 400)

    # if no such staff
    staff = Staff.getStaffByBarcode(barcode)
    if staff == None:
        return ResponseUtil.error(ServiceUtil.errorDataNotFound('No such a staff'), 401)

    # test if table is closed
    if table.table_status == 0:
        return ResponseUtil.error(ServiceUtil.errorWrongLogic('Inactive table'), 400)

    # test if table occupied by POS
    if table.staff_id != 0 and table.staff_id is not None:
        return ResponseUtil.error(ServiceUtil.errorWrongLogic('Table is using by POS'), 412)

    # find the Salesorder
    salesorder = Salesorder.getSalesorderByTableCode(tableCode)
    if UtilValidate.isEmpty(salesorder):
        return ResponseUtil.error(ServiceUtil.errorWrongLogic('No order found', code=3001))

    # do not return invalid salesorder (when status is 10, 11)
    if salesorder.status == 10 or salesorder.status == 11:
        return ResponseUtil.error(ServiceUtil.errorWrongLogic('No order found', code=3001))

    # put Salesorder lines to data
    data = {}
    data['open-sales'] = []
    # data['always-return-outcome'] = 'true'
    salesorderJson = {
        'amount': str(salesorder.subtotal).replace('.', ''),
        'pos-reference': salesorder.salesorder_id,
        'table': table.table_code
    }
    data['open-sales'].append(salesorderJson)

    return ResponseUtil.tyro_success(data)


@tyro_blueprint.route('/transaction-result', methods=['POST'])
def transactionResult():
    transactionResult = json.loads(flask.request.data)

    result = transactionResult.get('result')
    mid = transactionResult.get('mid')
    tid = transactionResult.get('tid')
    operatorId = transactionResult.get('operator-id')
    table = transactionResult.get('table')
    approvalCode = transactionResult.get('approval-code')
    posReference = transactionResult.get('pos-reference')
    issuerActionCode = transactionResult.get('issuer-action-code')
    responseMessage = transactionResult.get('response-message')
    tipAmount = transactionResult.get('tip-amount')
    baseAmount = transactionResult.get('base-amount')
    baseCurrency = transactionResult.get('base-currency ')
    cardCurrency = transactionResult.get('card-currency ')
    cardType = transactionResult.get('card-type ')
    elidedPan = transactionResult.get('elided-pan ')
    gstPercentage = transactionResult.get('gst-percentage')
    operatorId = transactionResult.get('operator-id ')
    panLength = transactionResult.get('pan-length ')
    rrn = transactionResult.get('rrn ')
    surchargeAmount = transactionResult.get('surcharge-amount ')
    terminalTransactionLocalDateTime = transactionResult.get('terminal-transaction-local-date-time ')
    transactionReference = transactionResult.get('transaction-reference ')
    transactionType = transactionResult.get('transaction-type ')
    transmissionDateTime = transactionResult.get('transmission-date-time ')
    transactionAmount = transactionResult.get('transaction-amount ')
    transactionCurrency = transactionResult.get('transaction-currency ')
    exchangeRate = transactionResult.get('exchange-rate ')
    receiptBlock = transactionResult.get('receipt-block ')

    data = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'

    return ResponseUtil.tyro_success(data)
