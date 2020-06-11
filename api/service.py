from utils import ResponseUtil, ServiceUtil, UtilValidate
from models import Tables, Keyboard, KeyboardCat, KeyboardItem, Stock, Category, ExtraStock, TasteStock, Staff, \
	Salesorder, SalesorderLine, Site, StockPrint, CatPrint, KeyboardPrint, Kitchen, Docket, DocketLine, Payment
import json


class SalesorderService():

	@staticmethod
	def newSalesorder(context: dict) -> dict:
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
			transaction = 'TA'

		if isPaid:
			status = 11
		else:
			status = 1

		# insert a new salesorder
		salesorderId, tableCode = Salesorder.insertSalesorder(tableCode, guestNo, staffId,
												   UtilValidate.tsToTime(UtilValidate.getCurrentTs()),
												   transaction, status)

		ResponseUtil.success(result, {"salesorderId": salesorderId, "tableCode":tableCode})

		return result


class SalesorderLineService():

	@staticmethod
	def insertSalesorderLine(context: dict) -> dict:
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

		if UtilValidate.isEmpty(salesorderId):
			return ResponseUtil.errorMissingParameter(result, 'salesorderId')


		# test if given sales order Id is the one attached to table
		salesorder = Salesorder.getSalesorderByTableCode(tableCode)
		if UtilValidate.isEmpty(salesorder):
			return ResponseUtil.errorDataNotFound(result, "No such table/order")

		if salesorder.salesorder_id != int(salesorderId):
			return ResponseUtil.errorWrongLogic(result, 'Given salesorderId is not matched to table record',
												code=3002)

		salesorderLines = json.loads(salesorderLines)
		if goToKitchen:
			status = 1
		else:
			status = 0

		purchaseQuantity = 1

		for line in salesorderLines:
			if len(line) != 7:
				return ResponseUtil.errorWrongLogic(result, 'Incorrect content', code=3003)

			stockId = line["stockId"]
			stock = Stock.getByStockId(stockId)
			sizeLevel = line["sizeLevel"]
			quantity = line["quantity"]
			purchaseQuantity = int(quantity)
			price = line["price"]

			parentlineId = 0
			originalSalesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, stockId, sizeLevel, price,
																		   quantity, staffId,
																		   UtilValidate.tsToTime(
																			   UtilValidate.getCurrentTs()),
																		   parentlineId, status)

			for extra in line["extra"]:
				parentlineId = 2
				sizeLevel = 0
				quantity = extra["quantity"] * purchaseQuantity
				price = extra["price"]
				extraId = extra["stockId"]
				salesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, extraId, sizeLevel, price, quantity,
																	   staffId, UtilValidate.tsToTime(
						UtilValidate.getCurrentTs()), parentlineId, status, orderlineId=originalSalesorderLineId)

			for taste in line["taste"]:
				parentlineId = 1
				sizeLevel = 0
				quantity = taste["quantity"] * purchaseQuantity
				price = taste["price"]
				extraId = taste["stockId"]
				salesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, extraId, sizeLevel, price, quantity,
																	   staffId, UtilValidate.tsToTime(
						UtilValidate.getCurrentTs()), parentlineId, status, orderlineId=originalSalesorderLineId)


			comments = line["comments"]

			# TODO TEST
			if goToKitchen:
				try:
					printers = SalesorderLineService.findPrinter(stockId)
				except Exception as inst:
					return ResponseUtil.errorDataNotFound(result, inst.args[0])

				today = UtilValidate.tsToToday(UtilValidate.getCurrentTs())
				firstOrder = Salesorder.getFirstOrderToday(today)
				unit = int(salesorderId) - firstOrder.salesorder_id + 1
				SalesorderLineService.insertKitchen(printers, originalSalesorderLineId, comments, tableCode, unit)


		Salesorder.updatePrice(salesorderId)

		ResponseUtil.success(result)

		return result

	@staticmethod
	def calculateSalesorderLine(context: dict) -> dict:
		result = ServiceUtil.returnSuccess()

		token = context.get('token')
		salesorderLines = context.get('salesorderLines')


		if token is None or salesorderLines is None:
			return ResponseUtil.errorMissingParameter(result)

		tokenValid, staffId = UtilValidate.tokenValidation(token)
		if not tokenValid:
			return ResponseUtil.errorSecurityNotLogin(result, 'Invalid token')

		salesorderLines = json.loads(salesorderLines)

		total = 0

		for line in salesorderLines:
			if len(line) != 7:
				return ResponseUtil.errorWrongLogic(result, 'Incorrect content', code=3003)

			stockId = line["stockId"]
			stock = Stock.getByStockId(stockId)
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

			total = total + Stock.getPrice(stock, price) * quantity


			for extra in line["extra"]:
				stock = Stock.getByStockId(extra["stockId"])
				price = stock.sell

				quantity = extra["quantity"]
				total = total + Stock.getPrice(stock, price) * quantity

			for taste in line["taste"]:
				stock = Stock.getByStockId(taste["stockId"])
				price = stock.sell
				quantity = taste["quantity"]
				total = total + Stock.getPrice(stock, price) * quantity

		ResponseUtil.success(result, {"salesorderTrialPrice": total})

		return result





	@staticmethod
	def findPrinter(stockId):
		# find activate keyboard
		keyboard = Keyboard.getActivateKeyboard()
		kbId = keyboard.kb_id
		stock = Stock.getByStockId(stockId)

		# find keyboard item
		keyboardItem = KeyboardItem.getByBarcodeAndKbId(stock.barcode, kbId)
		if UtilValidate.isEmpty(keyboardItem):
			raise Exception('keyboardItem does not have matched item.')
		kbCatId = keyboardItem.cat_id

		# get keyboard Cat
		keyboardCat = KeyboardCat.getByCatIdAndKbId(kbCatId, kbId)
		catName = keyboardCat.cat_name

		#get cat name from keyboard cat and find it from category's cat id
		catId = Category.getByCatName(catName).cat_id

		# try stock print
		printer = StockPrint.getPrinter(stockId)

		if printer: return printer

		# try category printer
		printer = CatPrint.getPrinter(catId)

		if printer: return printer

		# try keyboard printer
		printer = KeyboardPrint.getPrinter(kbId)

		if printer: return printer

		raise Exception('Stock的printer没有正确配置. Stock id = {}'.format(stockId))


	@staticmethod
	def insertKitchen(printers, originalSalesorderLineId, comments, tableCode, unit):
		# salesorderLine is the original food
		# salesorderLines including the extra and taste, but all them need to go to kitchen

		salesorderLines = SalesorderLine.getByOrderlineId(originalSalesorderLineId)

		for salesorderLine in salesorderLines:
			stock = Stock.getByStockId(salesorderLine.stock_id)
			for printer in printers:
				# hotFIX
				deliveryDocket = printer.delivery_docket
				lineId = salesorderLine.line_id
				orderlineId = salesorderLine.orderline_id
				salesorderId = salesorderLine.salesorder_id
				# TODO FIX FOR TAKEAWAY ORDER
				tableCode = tableCode
				cat1 = stock.cat1
				description = stock.description
				description2 = stock.description2
				if salesorderLine.size_level == 1:
					description = stock.custom1 + " " + description
					description2 = stock.custom1 + " " +  description2

				if salesorderLine.size_level == 2:
					description = stock.custom2 + " " +  description
					description2 = stock.custom2 + " " +  description2

				if salesorderLine.size_level == 3:
					description = stock.custom3 + " " +  description
					description2 = stock.custom3 + " " +  description2

				if salesorderLine.size_level == 4:
					description = stock.custom4 + " " +  description
					description2 = stock.custom4 + " " +  description2

				quantity = salesorderLine.quantity
				orderTime = salesorderLine.time_ordered
				cat2 = stock.cat2
				printerName = printer.printer
				stockType = salesorderLine.parentline_id
				comments = comments
				# TODO FIXME staff_ID is not right
				staffName = salesorderLine.staff_id

				if stockType != 0: comments = ""
				if deliveryDocket:
					printerName = "+" + printerName

				lineId = Kitchen.insertKitchen(lineId, orderlineId, tableCode, staffName, cat1, description, description2,
											   unit, quantity, printerName, orderTime, comments, stockType, cat2, salesorderId)


class DocketService():

	@staticmethod
	def newDocket(context: dict) -> dict:
		result = ServiceUtil.returnSuccess()

		token = context.get('token')
		tableCode = context.get('tableCode')
		subtotal = context.get('subtotal')
		guestNo = context.get('guestNo')

		if token is None:
			return ResponseUtil.errorMissingParameter(result)

		# verifying token
		tokenValid, staffId = UtilValidate.tokenValidation(token)
		if not tokenValid:
			return ResponseUtil.errorSecurityNotLogin(result, 'Invalid token')



		docketId = Docket.insertDocket(UtilValidate.tsToTime(UtilValidate.getCurrentTs()), staffId, tableCode, subtotal, guestNo)

		ResponseUtil.success(result, {"docketId": docketId})

		return result


class DocketLineService():

	@staticmethod
	def insertDocketLine(context: dict) -> dict:
		result = ServiceUtil.returnSuccess()

		docketId = context.get('docketId')
		salesorderId = context.get('salesorderId')

		lines = SalesorderLine.getBySalesorderId(salesorderId)
		for line in lines:
			DocketLine.insertDocketLine(docketId, line.stock_id, line.size_level, float(line.sell_inc), line.quantity)

		return result

class PaymentService():

	@staticmethod
	def insertPayment(context: dict) -> dict:
		result = ServiceUtil.returnSuccess()
		docketId = context.get('docketId')
		paymentDetail = context.get('paymentDetail')

		for payment in paymentDetail:
			Payment.insertPayment(docketId, UtilValidate.tsToTime(UtilValidate.getCurrentTs()), payment["paymentType"], float(payment["amount"]))

		return result