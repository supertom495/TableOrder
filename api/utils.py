import sys
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import os

class UtilValidate:
	def __init__(self):
		pass

	@staticmethod
	def isNotEmpty(lst:list) -> bool:
		return lst is not None and len(lst)!=0

	@staticmethod
	def isEmpty(lst:list) -> bool:
		return not lst

	@staticmethod
	def encryption(privateInfo):
		# 32 bytes = 256 bits
		# 16 = 128 bits
		# the block size for cipher obj, can be 16 24 or 32. 16 matches 128 bit.
		BLOCK_SIZE = 16
		# the character used for padding
		# used to ensure that your value is always a multiple of BLOCK_SIZE
		PADDING = '{'
		# function to pad the functions. Lambda
		# is used for abstraction of functions.
		# basically, its a function, and you define it, followed by the param
		# followed by a colon,
		# ex = lambda x: x+5
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
		print(decoded)
		return decoded


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
	def success(result:dict) -> dict:
		result["code"] = "0"
		result["message"] = "success"
		return result

	@staticmethod
	def success(result:dict, data) -> dict:
		result["code"] = "0"
		result["message"] = "success"
		result["data"] = data
		return result

	@staticmethod
	def errorDataNotFound(result:dict, message) -> dict:
		result["code"] = ResponseUtil.ERROR_DATA_NOT_FOUND
		result["message"] = "ERROR_DATA_NOT_FOUND" + " : " + message
		return result