import sys
import os
import posOperation
import common
common.setVar()


def testPrinter(lineId):
    res = posOperation.findPrinter(lineId)


def testActivateTable(tableId):
    res = posOperation.activateTable(tableId)


def testCatPrint(catId):
    catPrint = posOperation.getCatPrint(catId)
    for i in catPrint:
        a = i
        print(a)


testCatPrint(3)

# print( posOperation.getActiveSaleOrdersByTableCode("02"))
