import requests
import json
import common


def testResponse(response, methodName):
    if response.status_code >= 400:
        common.logging("Fail to {}".format(methodName) +
                       "\n" + "Reason: {}".format(response.text + "\n\n"))


def addOption(data):
    url = "{}/stockoption".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.post(url,
                             data=data, headers=header)

    testResponse(response, "add option")

    return response


def addStock(data):
    url = "{}/stock".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.post(url,
                             data=data, headers=header)

    testResponse(response, "add stock")

    return response


def addKeyboard(data):
    url = "{}/keyboard".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.post(url,
                             data=data, headers=header)

    testResponse(response, "add keyboard")

    return response


def activateKeyboard(kbId):
    url = "{}/keyboard/{}".format(common.URLPREFIX, kbId)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.put(url, headers=header)

    testResponse(response, "activate keyboard")

    return response


def addKeyboardCat(data):
    url = "{}/keyboardcat".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.post(url,
                             data=data, headers=header)

    testResponse(response, "add keyboard category")

    return response


def addKeyboardItem(data):
    url = "{}/keyboarditem".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.post(url,
                             data=data, headers=header)

    testResponse(response, "add keyboard items")

    return response


def listKeyboard():
    url = "{}/keyboard".format(common.URLPREFIX)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=header)

    testResponse(response, "list keyboard")

    return response


def addTable(data):
    url = "{}/table".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.post(url,
                             data=data, headers=header)

    testResponse(response, "add table")

    return response


def deleteTable():
    url = "{}/table".format(common.URLPREFIX)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.delete(url, headers=header)

    testResponse(response, "delete table")
    return response


def addSalesOrder(data):
    url = "{}/salesorder".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.post(url,
                             data=data, headers=header)

    testResponse(response, "add salesorder")

    return response


def deleteSalesOrder(salesorderId):
    url = "{}/salesorder/{}".format(common.URLPREFIX, salesorderId)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.delete(url,
                               headers=header)

    testResponse(response, "delete salesorder by salesorderId{}".format(salesorderId))

    return response


def addSalesorderLine(data):
    url = "{}/salesorderline".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.post(url,
                             data=data, headers=header)

    testResponse(response, "add salesorder line")

    return response


def removeSalesorderLine(data):
    url = "{}/salesorderline".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.delete(url,
                               data=data, headers=header)

    testResponse(response, "remove salesorder line")

    return response


def getSalesorderLine(data):
    url = "{}/salesorderline".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.patch(url,
                              data=data, headers=header)

    testResponse(response, "retrive salesorder line online")

    return response


def updateSalesorderLine(data):
    url = "{}/salesorderline".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.put(url,
                            data=data, headers=header)

    testResponse(response, "update salesorder line")

    return response


def getToken():
    url = "{}/token".format(common.URLPREFIX)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=header)

    testResponse(response, "get token")

    return response


def refreshToken():
    url = "{}/token".format(common.URLPREFIX)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.put(url, headers=header)

    testResponse(response, "refresh token")

    return response


def uploadStockImage(data, file):
    url = "{}/image".format(common.URLPREFIX)

    response = requests.post(url, data=data, files={'file': file})

    testResponse(response, "upload image")

    return response


def addStaff(data):
    url = "{}/staff".format(common.URLPREFIX)
    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.post(url,
                             data=data, headers=header)

    testResponse(response, "add staff")

    return response
