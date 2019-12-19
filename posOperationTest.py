import common
import posOperation


common.setVar()

def testPrinter(lineId):
    res = posOperation.findPrinter(lineId)


def testActivateTable(tableId):
    res = posOperation.activateTable(tableId)



print( posOperation.getActiveSaleOrdersByTableCode("02"))
