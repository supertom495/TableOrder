class ServiceUtil:
	def __init__(self):
		pass

	@staticmethod
	def returnSuccess() -> dict:
		result = {}
		result["code"] = 0
		result["message"] = "success"
		return result

