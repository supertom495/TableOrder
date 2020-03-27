import base64
from Crypto.Cipher import AES
import time
from models import Staff


class UtilValidate:
	def __init__(self):
		pass

	@staticmethod
	def isNotEmpty(data) -> bool:
		if type(data) is list:
			return data is not None and len(data)!=0


	@staticmethod
	def isEmpty(data) -> bool:
		return not data

	# format match the api requirement
	@staticmethod
	def getCurrentTs():
		return int(round(time.time()))


	@staticmethod
	def tsToTime(ts):
		ts = int(ts)
		# ts /= 1000
		t = time.localtime(ts)
		docketDate = time.strftime("%Y-%m-%d %H:%M:%S", t)
		# docketDate += ".000"
		return docketDate


	@staticmethod
	def encryption(privateInfo):
		# 32 bytes = 256 bits # 16 = 128 bits
		# the block size for cipher obj, can be 16 24 or 32. 16 matches 128 bit.
		BLOCK_SIZE = 16
		# the character used for padding
		# used to ensure that your value is always a multiple of BLOCK_SIZE
		PADDING = '{'
		# function to pad the functions. Lambda
		# is used for abstraction of functions.
		# basically, its a function, and you define it, followed by the param
		# followed by a colon,  ex = lambda x: x+5
		pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
		# encrypt with AES, encode with base64
		EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
		# generate a randomized secret key with urandom
		secret = b'\xdb\xb1?\xe2\xeb7\x9b\xa5b\x9erA\xfcP\xbb='
		print('encryption key:', secret)
		# creates the cipher obj using the key
		cipher = AES.new(secret)
		# encodes you private info!
		encoded = EncodeAES(cipher, privateInfo)
		print('Encrypted string:', encoded)
		return encoded

	@staticmethod
	def decryption(encryptedString):
		PADDING = b'{'
		DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
		# Key is FROM the printout of 'secret' in encryption
		# below is the encryption.
		encryption = encryptedString
		key = b'\xdb\xb1?\xe2\xeb7\x9b\xa5b\x9erA\xfcP\xbb='
		cipher = AES.new(key)
		decoded = DecodeAES(cipher, encryption)
		# print(decoded)
		return decoded

	@staticmethod
	def tokenValidation(token):
		plainText = UtilValidate.decryption(token).decode('UTF-8')
		timestamp = plainText[-10:]
		staffBarcode = plainText[:-10]
		if timestamp < str(int(time.time())):
			return False, None
		staff = Staff.getStaffByBarcode(staffBarcode)
		if staff == None:
			return False, None

		return True, staff.staff_id




class ServiceUtil:
	def __init__(self):
		pass

	@staticmethod
	def returnSuccess() -> dict:
		result = {}
		result["code"] = "0"
		result["message"] = "success"
		return result



class ResponseUtil:
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
	def success(result:dict, data=None) -> dict:
		result["code"] = "0"
		result["message"] = "success"
		if data is not None:
			result["data"] = data
		return result

	@staticmethod
	def errorDataNotFound(result:dict, message) -> dict:
		result["code"] = ResponseUtil.ERROR_DATA_NOT_FOUND
		result["message"] = "ERROR_DATA_NOT_FOUND" + " : " + message
		return result

	@staticmethod
	def errorWrongLogic(result:dict, message, code=ERROR_WRONG_LOGIC) -> dict:
		result["code"] = code
		result["message"] = "ERROR_WRONG_LOGIC" + " : " + message
		return result

	@staticmethod
	def errorSecurityNotLogin(result:dict, message) -> dict:
		result["code"] = ResponseUtil.ERROR_SECURITY_NOT_LOGIN
		result["message"] = "ERROR_SECURITY_NOT_LOGIN" + " : " + message
		return result

	@staticmethod
	def errorMissingParameter(result:dict, message="") -> dict:
		result["code"] = ResponseUtil.ERROR_MISSING_PARAMETER
		result["message"] = "ERROR_MISSING_PARAMETER" + " : " + message
		return result

	@staticmethod
	def errorInvalidParameter(result:dict, message) -> dict:
		result["code"] = ResponseUtil.ERROR_INVALID_PARAMETER
		result["message"] = "ERROR_INVALID_PARAMETER" + " : " + message
		return result