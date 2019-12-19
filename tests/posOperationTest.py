import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import common
import posOperation

common.setVar()

def testPrinter(lineId):
    res = posOperation.findPrinter(lineId)


def testActivateTable(tableId):
    res = posOperation.activateTable(tableId)



# print( posOperation.getActiveSaleOrdersByTableCode("02"))
