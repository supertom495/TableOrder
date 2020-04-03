from utils import ResponseUtil, ServiceUtil, UtilValidate
from models import Tables, Keyboard, KeyboardCat, KeyboardItem, Stock, Category, ExtraStock, TasteStock, Staff, Salesorder, SalesorderLine, Site
import json

class salesorderService():

	@staticmethod
	def newSalesorder(context:dict) -> dict:
		result = ServiceUtil.returnSuccess()

		token = context.get('token')
		tableCode = context.get('tableCode')
		guestNo = context.get('guestNo')
		isPaid = context.get('isPaid')


		if token is None:
			return ResponseUtil.errorMissingParameter(result)

		# verifying token
		tokenValid, staffId = UtilValidate.tokenValidation(token)
		if not tokenValid:
			return ResponseUtil.errorSecurityNotLogin(result, 'Invalid token')

		if tableCode:
			table = Tables.getTableByTableCode(tableCode)
			# test if table exists
			if UtilValidate.isEmpty(table):
				return ResponseUtil.errorDataNotFound(result, 'Wrong table code')

			# test if table occupied by POS
			if table.staff_id != 0 and table.staff_id is not None:
				return ResponseUtil.errorWrongLogic(result, 'Fail to open table, table is using by POS')

			# test if table is already opened
			if table.table_status != 0:
				return ResponseUtil.errorWrongLogic(result, 'Fail to open table, table is already opened', code=3001)

			# Activate Table
			Tables.activateTable(tableCode, UtilValidate.tsToTime(UtilValidate.getCurrentTs()))
			transaction = 'DI'

		else:
			tableCode = 'TA-5'
			transaction = 'TA'

		if isPaid:
			status = 11
		else:
			status = 0


		# insert a new salesorder
		salesorderId = Salesorder.insertSalesorder(tableCode, guestNo, staffId,
												   UtilValidate.tsToTime(UtilValidate.getCurrentTs()),
												   transaction, status)

		ResponseUtil.success(result, {"salesorderId": salesorderId})

		return result


class salesorderLineService():

	@staticmethod
	def insertSalesorderLine(context:dict) -> dict:
		result = ServiceUtil.returnSuccess()

		token = context.get('token')
		tableCode = context.get('tableCode')
		salesorderId = context.get('salesorderId')
		salesorderLines = context.get('salesorderLines')
		goToKitchen = context.get('goToKitchen')

		if token is None or salesorderId is None or salesorderLines is None:
			return ResponseUtil.errorMissingParameter(result)


		tokenValid, staffId = UtilValidate.tokenValidation(token)
		if not tokenValid:
			return ResponseUtil.errorSecurityNotLogin(result, 'Invalid token')

		if tableCode:
			table = Tables.getTableByTableCode(tableCode)
			# test if table exists
			if UtilValidate.isEmpty(table):
				return ResponseUtil.errorDataNotFound(result, 'Wrong table code')

			# test if table is closed
			if table.table_status == 0:
				return ResponseUtil.errorWrongLogic(result, 'Inactive table')

			# test if table occupied by POS
			if table.staff_id != 0 and table.staff_id is not None:
				return ResponseUtil.errorWrongLogic(result, 'Fail to add dishes, table is using by POS', code=3001)

			# test if given sales order Id is the one attached to table
			salesorder = Salesorder.getSalesorderByTableCode(tableCode)
			if salesorder.salesorder_id != int(salesorderId):
				return ResponseUtil.errorWrongLogic(result, 'Given salesorderId is not matched to table record', code=3002)


		salesorderLines = json.loads(salesorderLines)

		if goToKitchen:
			status = 1
		else:
			status = 0


		for line in salesorderLines:
			if len(line) != 6:
				return ResponseUtil.errorWrongLogic(result, 'Incorrect content', code=3003)

			stockId = line["stockId"]
			stock = Stock.getStockById(stockId)
			sizeLevel = line["sizeLevel"]
			quantity = line["quantity"]
			price = stock.sell
			if sizeLevel == 0 or sizeLevel == 1:
				price = stock.sell
			if sizeLevel == 2:
				price = stock.sell2
			if sizeLevel == 3:
				price = stock.sell3
			if sizeLevel == 4:
				price = stock.sell4

			parentlineId = 0
			originalSalesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, stockId, sizeLevel, price,
																		   quantity, staffId,
																		   UtilValidate.tsToTime(UtilValidate.getCurrentTs()),
																		   parentlineId, status)
			if goToKitchen:
				pass
				# goToKitchen()

			for extra in line["extra"]:
				parentlineId = 2
				sizeLevel = 0
				price = Stock.getStockById(extra).sell
				quantity = 1
				salesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, extra, sizeLevel, price, quantity,
																	   staffId, UtilValidate.tsToTime(
						UtilValidate.getCurrentTs()), parentlineId, status, orderlineId=originalSalesorderLineId)
			if goToKitchen:
				pass
				# goToKitchen()

			for taste in line["taste"]:
				parentlineId = 1
				sizeLevel = 0
				price = Stock.getStockById(taste).sell
				quantity = 1
				salesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, taste, sizeLevel, price, quantity,
																	   staffId, UtilValidate.tsToTime(
						UtilValidate.getCurrentTs()), parentlineId, status, orderlineId=originalSalesorderLineId)
			if goToKitchen:
				pass
				# goToKitchen()

			comments = line["comments"]

		Salesorder.updatePrice(salesorderId)

		ResponseUtil.success(result)

		return result
