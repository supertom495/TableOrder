import json
from tool.utils import ServiceUtil, UtilValidate
from model.BasicModel import Tables, Keyboard, Stock, Category, Salesorder, SalesorderLine, StockPrint, \
    CatPrint, KeyboardPrint, Kitchen, Docket, DocketLine, Payment, SalesorderOnline, SalesorderLineOnline, DocketOnline


class SalesorderService():

    @staticmethod
    def newSalesorder(context: dict) -> dict:
        # result = ServiceUtil.returnSuccess()

        staffId = context.get('staffId')
        tableCode = context.get('tableCode')
        guestNo = context.get('guestNo')
        isPaid = context.get('isPaid')
        remark = context.get('remark')
        actualId = context.get('actualId')


        if tableCode:
            table = Tables.getTableByTableCode(tableCode)
            # test if table exists
            if UtilValidate.isEmpty(table):
                return ServiceUtil.errorDataNotFound('Wrong table code')

            # test if table occupied by POS
            # if table.staff_id != 0 and table.staff_id is not None:
            # 	return ServiceUtil.errorWrongLogic('Fail to open table, table is using by POS')

            # test if table is already opened
            if table.table_status != 0:
                return ServiceUtil.errorWrongLogic('Fail to open table, table is already opened', code=3001)

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

        SalesorderOnline.insertSalesorderOnline(salesorderId, actualId, remark, status)

        result = ServiceUtil.returnSuccess({"salesorderId": salesorderId, "tableCode": tableCode})

        return result


class SalesorderLineService():

    @staticmethod
    def insertSalesorderLine(context: dict) -> dict:
        # result = ServiceUtil.returnSuccess()

        staffId = context.get('staffId')
        tableCode = context.get('tableCode')
        salesorderId = context.get('salesorderId')
        salesorderLines = context.get('salesorderLines')
        goToKitchen = context.get('goToKitchen')
        actualId = context.get('actualId')

        if salesorderId is None or salesorderLines is None:
            return ServiceUtil.errorMissingParameter()

        if UtilValidate.isEmpty(salesorderId):
            return ServiceUtil.errorMissingParameter('salesorderId')

        # test if given sales order Id is the one attached to table
        salesorder = Salesorder.getSalesorderByTableCode(tableCode)
        if UtilValidate.isEmpty(salesorder):
            return ServiceUtil.errorDataNotFound("No such table/order")

        if salesorder.salesorder_id != int(salesorderId):
            return ServiceUtil.errorWrongLogic('Given salesorderId is not matched to table record',
                                               code=3002)

        table = Tables.getTableByTableCode(tableCode)
        if tableCode[0:2] != 'TA':
            # test if table exists
            if UtilValidate.isEmpty(table):
                return ServiceUtil.errorDataNotFound('Wrong table code')

            # test if table occupied by POS
            if table.staff_id != 0 and table.staff_id is not None:
                return ServiceUtil.errorWrongLogic('Fail to add dish, table is using by POS')

        salesorderLines = json.loads(salesorderLines)
        if goToKitchen:
            status = 1
        else:
            status = 0

        purchaseQuantity = 1

        # get the table site for print
        if UtilValidate.isNotEmpty(table):
            tableSiteId = table.site_id
        else:
            tableSiteId = -1

        inactiveStockIds = []

        for line in salesorderLines:
            if len(line) < 7:
                return ServiceUtil.errorWrongLogic('Incorrect content', code=3003)

            stockId = line['stockId']
            actualLineId = line.get('actualLineId')
            stock = Stock.getByStockId(stockId)
            if stock.inactive == 1 and stock.barcode != 'KIOSKDELIVERY':
                inactiveStockIds.append(stockId)
            sizeLevel = line["sizeLevel"]
            quantity = line["quantity"]
            purchaseQuantity = int(quantity)
            price = line["price"]

            parentlineId = 0
            if sizeLevel == 5:
                originalSalesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, stockId, 3, price,
                                                                               quantity, staffId,
                                                                               UtilValidate.tsToTime(
                                                                                   UtilValidate.getCurrentTs()),
                                                                               parentlineId, status)
                parentlineId = 1
                sizeLevel = 0
                quantity =  purchaseQuantity
                price = 0
                tasteId = 102
                salesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, tasteId, sizeLevel, price,
                                                                       quantity,
                                                                       staffId, UtilValidate.tsToTime(
                        UtilValidate.getCurrentTs()), parentlineId, status, orderlineId=originalSalesorderLineId)


            else:
                originalSalesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, stockId, sizeLevel, price,
                                                                               quantity, staffId,
                                                                               UtilValidate.tsToTime(
                                                                                   UtilValidate.getCurrentTs()),
                                                                               parentlineId, status)
            # 线上记录
            SalesorderLineOnline.insertSalesorderLineOnline(originalSalesorderLineId, salesorderId, actualId,
                                                            actualLineId, stockId, quantity, sizeLevel, status, 'main')

            for extra in line["extra"]:
                parentlineId = 2
                sizeLevel = 0
                quantity = extra["quantity"] * purchaseQuantity
                price = extra["price"]
                extraId = extra["stockId"]
                salesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, extraId, sizeLevel, price,
                                                                       quantity,
                                                                       staffId, UtilValidate.tsToTime(
                        UtilValidate.getCurrentTs()), parentlineId, status, orderlineId=originalSalesorderLineId)
            # SalesorderLineOnline.insertSalesorderLineOnline(originalSalesorderLineId, salesorderId, actualId, extraId, quantity, sizeLevel, status, 'extra')

            for taste in line["taste"]:
                parentlineId = 1
                sizeLevel = 0
                quantity = taste["quantity"] * purchaseQuantity
                price = taste["price"]
                tasteId = taste["stockId"]
                salesorderLineId = SalesorderLine.insertSalesorderLine(salesorderId, tasteId, sizeLevel, price,
                                                                       quantity,
                                                                       staffId, UtilValidate.tsToTime(
                        UtilValidate.getCurrentTs()), parentlineId, status, orderlineId=originalSalesorderLineId)

            comments = line["comments"]

            if goToKitchen:
                printers = SalesorderLineService.findPrinter(stockId, tableSiteId)

                if printers is None:
                    continue

                today = UtilValidate.tsToToday(UtilValidate.getCurrentTs())
                firstOrder = Salesorder.getFirstOrderToday(today)
                if UtilValidate.isNotEmpty(firstOrder):
                    unit = int(salesorderId) - firstOrder.salesorder_id + 1
                else:
                    unit = 1
                SalesorderLineService.insertKitchen(printers, originalSalesorderLineId, comments, tableCode, unit)

        if len(inactiveStockIds) != 0:
            return ServiceUtil.errorInvalidParameter('Inactive stockId', data=inactiveStockIds)

        Salesorder.updatePrice(salesorderId)

        result = ServiceUtil.returnSuccess()

        return result

    @staticmethod
    def calculateSalesorderLine(context: dict) -> dict:
        # result = ServiceUtil.returnSuccess()

        staffId = context.get('staffId')
        salesorderLines = context.get('salesorderLines')

        if salesorderLines is None:
            return ServiceUtil.errorMissingParameter()

        salesorderLines = json.loads(salesorderLines)

        total = 0

        for line in salesorderLines:
            if len(line) != 7:
                return ServiceUtil.errorWrongLogic('Incorrect content', code=3003)

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

        result = ServiceUtil.returnSuccess({"salesorderTrialPrice": total})

        return result

    @staticmethod
    def findPrinter(stockId, siteId):
        # find activate keyboard
        keyboard = Keyboard.getActivateKeyboard()
        kbId = keyboard.kb_id
        stock = Stock.getByStockId(stockId)
        catName = stock.cat1

        # get cat name from keyboard cat and find it from category's cat id
        category = Category.getByCatName(catName)
        if UtilValidate.isEmpty(category):
            raise Exception(
                'Stock does not have matched category. (Stock\'s cat1 does not exist in Category) StockId:{}'.format(stockId))
        catId = category.cat_id

        # try stock print
        printer = StockPrint.getPrinter(stockId, siteId)

        if printer: return printer

        # try category printer
        printer = CatPrint.getPrinter(catId, siteId)

        if printer: return printer

        # try keyboard printer
        printer = KeyboardPrint.getPrinter(kbId, siteId)

        if printer: return printer

        return None

    # raise Exception('Stock printer did not setup. Stock id = {}'.format(stockId))

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
                tableCode = tableCode
                cat1 = stock.cat1
                description = stock.description
                description2 = stock.description2
                if salesorderLine.size_level == 1:
                    description = stock.custom1 + " " + description
                    description2 = stock.custom1 + " " + description2

                if salesorderLine.size_level == 2:
                    description = stock.custom2 + " " + description
                    description2 = stock.custom2 + " " + description2

                if salesorderLine.size_level == 3:
                    description = stock.custom3 + " " + description
                    description2 = stock.custom3 + " " + description2

                if salesorderLine.size_level == 4:
                    description = stock.custom4 + " " + description
                    description2 = stock.custom4 + " " + description2

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

                lineId = Kitchen.insertKitchen(lineId, orderlineId, tableCode, staffName, cat1, description,
                                               description2,
                                               unit, quantity, printerName, orderTime, comments, stockType, cat2,
                                               salesorderId)


class DocketService():

    @staticmethod
    def newDocket(context: dict) -> dict:
        # result = ServiceUtil.returnSuccess()

        staffId = context.get('staffId')
        tableCode = context.get('tableCode')
        subtotal = context.get('subtotal')
        guestNo = context.get('guestNo')
        remark = context.get('remark')
        actualId = context.get('actualId')
        memberBarcode = context.get('memberBarcode')

        docketId = Docket.insertDocket(UtilValidate.tsToTime(UtilValidate.getCurrentTs()), staffId, tableCode, subtotal,
                                       guestNo, memberBarcode)
        DocketOnline.insert(docketId, actualId, remark)

        result = ServiceUtil.returnSuccess({"docketId": docketId})

        return result


class DocketLineService():

    @staticmethod
    def insertDocketLine(context: dict) -> dict:
        docketId = context.get('docketId')
        salesorderId = context.get('salesorderId')

        lines = SalesorderLine.getBySalesorderId(salesorderId)
        for line in lines:
            DocketLine.insertDocketLine(docketId, line.stock_id, line.size_level, float(line.sell_inc), line.quantity)

        result = ServiceUtil.returnSuccess()
        return result


class PaymentService():

    @staticmethod
    def insertPayment(context: dict) -> dict:
        docketId = context.get('docketId')
        paymentDetail = context.get('paymentDetail')
        drawer = context.get('drawer')

        for payment in paymentDetail:
            Payment.insertPayment(docketId, UtilValidate.tsToTime(UtilValidate.getCurrentTs()), payment["paymentType"],
                                  float(payment["amount"]), drawer)

        result = ServiceUtil.returnSuccess()

        return result

    @staticmethod
    def completeOrder(context: dict) -> dict:
        staffId = context.get('staffId')
        paymentDetail = context.get('paymentDetail')
        tableCode = context.get('tableCode')
        guestNo = context.get('guestNo')
        remark = context.get('remark')
        actualId = context.get('actualId')
        memberBarcode = context.get('memberBarcode')
        salesorderId = context.get('salesorderId')
        drawer = context.get('drawer')


        paymentDetail = json.loads(paymentDetail)
        subtotal = 0
        for payment in paymentDetail:
            subtotal += float(payment["amount"])

        # insert into docket
        docketResult = DocketService.newDocket({"staffId": staffId, "tableCode": tableCode,
                                                "subtotal": subtotal, "guestNo": guestNo, "remark": remark,
                                                "actualId": actualId, "memberBarcode": memberBarcode})
        if docketResult["code"] != "0":
            return docketResult

        docketId = docketResult['data']['docketId']

        # insert into docket line
        docketLineResult = DocketLineService.insertDocketLine({"docketId": docketId, "salesorderId": salesorderId})

        if docketLineResult["code"] != "0":
            return docketLineResult

        # insert into payments
        paymentResult = PaymentService.insertPayment({"docketId": docketId, "paymentDetail": paymentDetail, "drawer": drawer})

        if paymentResult["code"] != "0":
            return paymentResult

        # shut the table down
        Tables.deactivateTable(tableCode)

        result = ServiceUtil.returnSuccess()
        return result