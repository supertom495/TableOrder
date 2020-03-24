class UtilValidate:
	def __init__(self):
		pass

	@staticmethod
	def isNotEmpty(lst:list) -> bool:
		return lst is not None and len(lst)!=0

	@staticmethod
	def isEmpty(lst:list) -> bool:
		return not lst


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