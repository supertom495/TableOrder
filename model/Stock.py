import posOperation

def getStockById(stockId):
	return posOperation.db_get("select stock_id, barcode, description, description2, sell from Stock where stock_id = {};".format(stockId))

def getStockTaste():
	return posOperation.db_get("select * from TasteStock;")

def getStockExtra():
	return posOperation.db_get("select * from ExtraStock;")