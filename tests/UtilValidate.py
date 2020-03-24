class UtilValidate:
	def __init__(self):
		pass

	@staticmethod
	def isNotEmpty(lst:list) -> bool:
		return lst==None or len(lst)==0

