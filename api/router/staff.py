import flask
from utils import ServiceUtil, ResponseUtil, UtilValidate
from models import Staff
import time

staff_blueprint = flask.Blueprint(
    'staff',
    __name__,
    url_prefix='/api/v1/staff'
)


@staff_blueprint.route('/stafftoken', methods=['PUT'])
def getStaffToken():
    # result = ServiceUtil.returnSuccess()

    barcode = flask.request.form.get('barcode')
    staff = Staff.getStaffByBarcode(barcode)
    if staff == None:
        return ResponseUtil.error(ServiceUtil.errorDataNotFound('no such a staff'))

    toBeEncrypted = barcode + str(int(time.time()) + 3600)

    cipherText = UtilValidate.encryption(toBeEncrypted).decode('UTF-8')

    result = ServiceUtil.returnSuccess({"token": cipherText})

    return ResponseUtil.success(result)
