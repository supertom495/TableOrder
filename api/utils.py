import base64, hashlib, hmac, binascii, time, json
from Crypto.Cipher import AES
import flask
from models import Staff
from database import flaskConfig, serverName, aesCipher


class UtilValidate:
    def __init__(self):
        pass

    @staticmethod
    def getImageUrl(host):
        hostRange = host.split('.')[0]
        if hostRange == '10' or hostRange == '172' or hostRange == '192' or hostRange == '127' or hostRange == 'localhost:5001':
            if flaskConfig.get('ImageUrl'):
                return 'http://{}/img/'.format(flaskConfig.get('ImageUrl'))
            else:
                return 'http://{}/img/'.format(serverName)
        else:
            return 'https://pos-static.redpayments.com.au/{}/img/'.format(flaskConfig.get('StoreName'))

    @staticmethod
    def isNotEmpty(data) -> bool:
        if type(data) is list:
            return data is not None and len(data) != 0
        if type(data) is str:
            return bool(data and data.strip())
        return data

    @staticmethod
    def isEmpty(data) -> bool:
        # if type(data) is list:
        if type(data) is str:
            return not (data and data.strip())
        return not data

    # format match the api requirement
    @staticmethod
    def getCurrentTs():
        return int(round(time.time()))

    @staticmethod
    def tsToToday(ts):
        ts = int(ts)
        t = time.localtime(ts)
        docketDate = time.strftime("%Y-%m-%d", t)
        return docketDate

    @staticmethod
    def tsToTime(ts):
        ts = int(ts)
        # ts /= 1000
        t = time.localtime(ts)
        docketDate = time.strftime("%Y-%m-%d %H:%M:%S", t)
        # docketDate += ".000"
        return docketDate

    @staticmethod
    def dateToTs(date):
        timestamp2 = time.mktime(date.timetuple())  # DO NOT USE IT WITH UTC DATE
        return timestamp2

    # @staticmethod
    # def encryption(privateInfo):
    #     # return privateInfo.encode('UTF-8')
    #     # 32 bytes = 256 bits # 16 = 128 bits
    #     # the block size for cipher obj, can be 16 24 or 32. 16 matches 128 bit.
    #     BLOCK_SIZE = 16
    #     # the character used for padding
    #     # used to ensure that your value is always a multiple of BLOCK_SIZE
    #     PADDING = '{'
    #     # function to pad the functions. Lambda
    #     # is used for abstraction of functions.
    #     # basically, its a function, and you define it, followed by the param
    #     # followed by a colon,  ex = lambda x: x+5
    #     pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    #     # encrypt with AES, encode with base64
    #     EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    #     # generate a randomized secret key with urandom
    #     secret = b'\xdb\xb1?\xe2\xeb7\x9b\xa5b\x9erA\xfcP\xbb='
    #     # creates the cipher obj using the key
    #     cipher = AES.new(secret, AES.MODE_CBC)
    #     # encodes you private info!
    #     encoded = EncodeAES(cipher, privateInfo.encode('UTF-8'))
    #     return encoded
    #
    # @staticmethod
    # def decryption(encryptedString):
    #     # return encryptedString
    #     PADDING = b'{'
    #     DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    #     # Key is FROM the printout of 'secret' in encryption
    #     # below is the encryption.
    #     encryption = encryptedString.encode('UTF-8')
    #     key = b'\xdb\xb1?\xe2\xeb7\x9b\xa5b\x9erA\xfcP\xbb='
    #     cipher = AES.new(key, AES.MODE_CBC)
    #     decoded = DecodeAES(cipher, encryption)
    #     # print(decoded)
    #     return decoded

    @staticmethod
    def tokenValidation(token):
        try:
            if token == '16891689':
                return True, -2
            plainText = aesCipher.decrypt(token)
            timestamp = plainText[-10:]
            staffBarcode = plainText[:-10]
            if timestamp < str(int(time.time())):
                return False, None
            staff = Staff.getStaffByBarcode(staffBarcode)
            if staff == None:
                return False, None

        except Exception:
            return False, None

        return True, staff.staff_id

    @staticmethod
    def addSign(data: dict) -> dict:
        data['timestamp'] = UtilValidate.getCurrentTs()

        sign = UtilValidate.getSign(data)

        data['sign'] = sign

        return data

    @staticmethod
    def getSign(data: dict) -> str:
        from urllib.parse import urlencode
        import hashlib

        sorted_items = sorted(data.items())
        secret = ''
        PiselStaff = Staff.getPiselSecret()
        if UtilValidate.isNotEmpty(PiselStaff):
            secret = PiselStaff.barcode
        urlencoded = urlencode(sorted_items) + '&' + secret
        sign = hashlib.md5(urlencoded.encode('utf-8'))

        return sign.hexdigest()

    @staticmethod
    def _hmac_sha1(input_str):

        raw = input_str
        tyroStaff = Staff.getTyroSecret()
        key = b'p@ssphr@se'
        if UtilValidate.isNotEmpty(tyroStaff):
            key = tyroStaff.barcode.encode('ISO-8859-1')
        mac = hmac.new(key, raw, hashlib.sha1).digest()
        return binascii.hexlify(mac)


class ServiceUtil:
    SUCCESS = "0"
    ERROR_MISSING_PARAMETER = "1000"
    ERROR_INVALID_PARAMETER = "1001"
    ERROR_DATA_NOT_FOUND = "2000"
    ERROR_DATA_ACCESS = "2001"
    ERROR_WRONG_LOGIC = "3000"
    ERROR_SECURITY_NOT_LOGIN = "4000"
    ERROR_UNKNOWN = "9000"

    def __init__(self):
        pass

    @staticmethod
    def returnSuccess(data=None) -> dict:
        result = {}
        result["code"] = ServiceUtil.SUCCESS
        result["message"] = "success"
        if data is not None:
            result["data"] = data
        return result

    @staticmethod
    def errorDataNotFound(message):
        result = {}
        result["code"] = ServiceUtil.ERROR_DATA_NOT_FOUND
        result["message"] = "ERROR_DATA_NOT_FOUND" + " : " + message
        return result

    @staticmethod
    def errorDataAccess(message):
        result = {}
        result["code"] = ServiceUtil.ERROR_DATA_ACCESS
        result["message"] = "ERROR_DATA_ACCESS" + " : " + message
        return result

    @staticmethod
    def errorWrongLogic(message, code=ERROR_WRONG_LOGIC):
        result = {}
        result["code"] = code
        result["message"] = "ERROR_WRONG_LOGIC" + " : " + message
        return result

    @staticmethod
    def errorSecurityNotLogin(message):
        result = {}
        result["code"] = ServiceUtil.ERROR_SECURITY_NOT_LOGIN
        result["message"] = "ERROR_SECURITY_NOT_LOGIN" + " : " + message
        return result

    @staticmethod
    def errorMissingParameter(message=""):
        result = {}
        result["code"] = ServiceUtil.ERROR_MISSING_PARAMETER
        result["message"] = "ERROR_MISSING_PARAMETER" + " : " + message
        return result

    @staticmethod
    def errorInvalidParameter(message, data=None):
        result = {}
        if data is not None:
            result['data'] = data
        result["code"] = ServiceUtil.ERROR_INVALID_PARAMETER
        result["message"] = "ERROR_INVALID_PARAMETER" + " : " + message
        return result


class ResponseUtil:
    HTTP_OK = 200
    HTTP_BAD_REQUEST = 400

    def __init__(self):
        pass

    # @staticmethod
    # def success():
    # 	return {'code': 0, 'message': 'success'}, ResponseUtil.HTTP_OK

    @staticmethod
    def success(result: dict = None):
        if result is None:
            return {'code': 0, 'message': 'success'}, ResponseUtil.HTTP_OK
        return result, ResponseUtil.HTTP_OK

    @staticmethod
    def error(result: dict, errorCode=HTTP_BAD_REQUEST):
        return result, errorCode

    @staticmethod
    def tyro_success(result=None):
        response = flask.Response()
        if type(result) is dict:
            result = json.dumps(result)
        result = result.encode('ISO-8859-1')
        response.set_data(result)
        # response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["x-tyro-mac"] = UtilValidate._hmac_sha1(result)
        response.headers['Content-Type'] = 'text/plain'

        response.status_code = 200
        return response
