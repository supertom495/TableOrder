import requests
import json
import random

def getToken(staffCode):
    url = "http://172.16.11.251:5001/api/v1/staff/stafftoken"

    form = {
        "barcode": staffCode
    }

    response = requests.put(url, data=form)
    return json.loads(response.text)


def postBody(token, guestNo, salesorderLines, paymentDetail):
    form = {
        "token": token,
        "guestNo": guestNo,
        "salesorderLines": json.dumps(salesorderLines),
        "isPaid": 'true',
        "gotoKitchen": 'true',
        "paymentDetail": json.dumps(paymentDetail)
    }

def getStock():
    url = "http://172.16.11.251:5001/stock"

    response = requests.get(url)

    return json.loads(response.text)

menu = getStock()

# 模拟点1-12道菜
dishNum = random.randint(1,12)
guestNum = int((dishNum+2)/3)
print('dishNum: ' + str(dishNum))
print('guestNum: ' + str(guestNum))

catNum = len(menu['data']['stock'])
print(catNum)

print(menu)

print(getToken(1))