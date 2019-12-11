import common
import posOperation


common.setVar()
res = posOperation.getStock()

for thing in res:

    stockId = thing[0]
    dateModified = thing[1]
    # print(stockId)
    # print(dateModified)
    posOperation.insertStockLastTimeModified(stockId, dateModified)
