import flask
from tool.utils import ServiceUtil, ResponseUtil
from model.BasicModel import Staff
import time
from database import aesCipher

staff_blueprint = flask.Blueprint(
    'staff',
    __name__,
    url_prefix='/api/v1/staff'
)


@staff_blueprint.route('/visits-counter/')
def visits():
    if 'visits' in flask.session:
        flask.session['visits'] = flask.session.get('visits') + 1  # reading and updating session data
    else:
        flask.session['visits'] = 1 # setting session data
    return "Total visits: {}".format(flask.session.get('visits'))

@staff_blueprint.route('/delete-visits/')
def delete_visits():
    flask.session.pop('visits', None) # delete visits
    return 'Visits deleted'

@staff_blueprint.route('/stafftoken', methods=['PUT'])
def getStaffToken():

    barcode = flask.request.form.get('barcode')
    staff = Staff.getStaffByBarcode(barcode)
    if staff == None:
        return ResponseUtil.error(ServiceUtil.errorDataNotFound('no such a staff'))

    toBeEncrypted = barcode + str(int(time.time()) + 3600)

    cipherText = aesCipher.encrypt(toBeEncrypted).decode('UTF-8')

    result = ServiceUtil.returnSuccess({"token": cipherText})

    return ResponseUtil.success(result)
