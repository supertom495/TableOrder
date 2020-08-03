import requests
import json
import random
from datetime import datetime

baseURL = "http://172.16.11.251:5001"

def getToken(staffCode):
    url = baseURL + "/api/v1/staff/stafftoken"

    form = {
        "barcode": staffCode
    }

    response = requests.put(url, data=form)
    return json.loads(response.text)['data']['token']


def createBody(token, guestNo, salesorderLines, paymentDetail):
    form = {
        "token": token,
        "guestNo": guestNo,
        "salesorderLines": json.dumps(salesorderLines),
        "isPaid": 'true',
        "gotoKitchen": 'false',
        "paymentDetail": json.dumps(paymentDetail)
    }
    return form

def getStock():
    url = url = baseURL + "/stock"

    response = requests.get(url)

    return json.loads(response.text)

menu = getStock()

def createOrder():
    token = getToken('1')
    # 模拟点1-12道菜
    dishNo = random.randint(1, 12)
    guestNo = int((dishNo + 2) / 3)

    salesorderLines = [
      {
        "stockId": 66,
        "taste": [],
        "extra": [],
        "sizeLevel": 0,
        "quantity": 1,
        "comments": "",
        "price": 4.2
      }
    ]

    total = 0
    order = ''
    for i in range(dishNo):
        # print(menu)
        catLen = len(menu['data']['stock'])
        catOrder = random.randint(0, catLen - 1)
        stockLen = len(menu['data']['stock'][catOrder]['stocks'])
        stockOrder = random.randint(0, stockLen - 1)
        dish = menu['data']['stock'][catOrder]['stocks'][stockOrder]
        quantity = random.randint(1,3)
        extra = []
        taste = []

        sizeLevel = 0
        price = dish['price']['0']

        if len(dish['price']) > 1:
            sizeLevel = random.randint(1,2)
            v = random.choice(list(dish['price'].keys()))
            if v == '0':
                v = '1'
            price = dish['price'][v][0]


        if len(dish['extra']) > 0:
            extra.append({
                "stockId": menu['data']['extra'][random.randint(1, len(menu['data']['extra']) - 1)]['stockId'],
                "price": 0,
                "quantity": 1
            })

        if len(dish['taste']) > 0:
            taste.append({
                "stockId": menu['data']['taste'][random.randint(1, len(menu['data']['taste']) - 1)]['stockId'],
                "price": 0,
                "quantity": 1
            })


        order += str(i) + '\t' + str(dish) + '\n'


        salesorderLines.append({
            "stockId": dish['stockId'],
            "taste": taste,
            "extra": extra,
            "sizeLevel": sizeLevel,
            "quantity": quantity,
            "comments": "",
            "price": price
        })
        total += price*quantity


    paymentDetail = [{"paymentType":"Cash","amount":total}]
    body = createBody(token, guestNo, salesorderLines, paymentDetail)

    url = url = baseURL + "/api/v1/order/salesorderprepay"

    fileName = datetime.now().strftime("%Y %m %d   %H %M %S --- ") + str(random.randint(1,193928383))

    with open(fileName, "w") as text_file:
        print('writing')
        text_file.write(order)

    response = requests.post(url, data=body)


    return json.loads(response.text)


import time
import threading

def worker(num):
    print('work-{}'.format(num))
    for i in range(2):
        a = createOrder()
        print(a)


for i in range(2):
    t = threading.Thread(target=worker, args=(i, )) # 启动了五个线程，要启动几个就循环几次
    t.start()

