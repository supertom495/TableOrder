import logging
import pysher
import sys
import pusher
import common
import json
import posOperation
import pollingDatabase
import threading
import os


def setLogger():
    # 创建一个logger,可以考虑如何将它封装
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(os.path.join(os.getcwd(), './API_data/websocketLog.txt'))
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    # 记录一条日志
    logger.info('program opened--------------------------------------------------------------')
    return logger


class PusherWebsocket:
    def __init__(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        ch = logging.StreamHandler(sys.stdout)
        root.addHandler(ch)

        self.logger = setLogger()

        self.receiver = pysher.Pusher(key=common.KEY, secure=common.SECURE, custom_host=common.HOST, port=common.PORT)
        self.sender = pusher.Pusher(app_id=common.APPID, key=common.KEY, secret=common.SECRET, ssl=common.SECURE,
                                    host=common.HOST, port=common.PORT)

        self.receiver.connection.bind('pusher:connection_established', self.connect_handler)
        self.receiver.connect()

    def open_table(self, data, *args, **kwargs):
        try:
            print("Channel Callback: %s" % data)
            print("Opening Table")
            data = json.loads(data)
            tableCode = data["tableCode"]
            guestNo = data["guestNo"]

            lock = threading.Lock()
            with lock:
                # test if table occupied by POS
                staffId = posOperation.getTableStaffId(tableCode)[0][0]
                if staffId != 0 and staffId is not None:
                    self.sender.trigger('littlenanjing', 'App\\Events\\OpenTableResult',
                                        {'staffId': data["staffId"], 'tableCode': tableCode, 'code': '-1',
                                         'message': 'Fail to open table, table is using by POS'})
                    return

                # test if table is already opened
                tableStatus = posOperation.getTableByTableCode(tableCode)[0][3]
                if tableStatus != 0:
                    self.sender.trigger('littlenanjing', 'App\\Events\\OpenTableResult',
                                        {'staffId': data["staffId"], 'tableCode': tableCode, 'code': '-2',
                                         'message': 'Fail to open table, table is already opened'})
                    return

                posOperation.activateTable(tableCode)
                salesorderId = posOperation.insertSalesorder(tableCode, guestNo, data["staffId"])

                table = posOperation.getTableByTableCode(tableCode)
                pollingDatabase.addTable(table)

                # send salesorder to api
                pollingDatabase.findSalesOrder(tableCode=tableCode)

                self.sender.trigger('littlenanjing', 'App\\Events\\OpenTableResult',
                                    {'staffId': data["staffId"], 'tableCode': tableCode, 'code': '0',
                                     'message': 'success', 'salesorderId': salesorderId})
        except:
            self.logger.exception("Exception Logged")

    def change_table(self, data, *args, **kwargs):
        try:
            print("Channel Callback: %s" % data)
            print("change Table")
            data = json.loads(data)
            fromTableCode = data["fromTableCode"]
            toTableCode = data["toTableCode"]
            staffId = data["staffId"]

            lock = threading.Lock()
            with lock:
                fromTable = posOperation.getTableByTableCode(fromTableCode)[0]
                toTable = posOperation.getTableByTableCode(toTableCode)[0]
                fromOrder = posOperation.getOrderDetailByTableCode(fromTableCode)
                if len(fromOrder) == 0:
                    self.sender.trigger('littlenanjing', 'App\\Events\\ChangeTableResult',
                                        {'staffId': data["staffId"], 'code': '-1', 'message': '此桌没有订单'})
                    return
                fromOrder = fromOrder[0]

                # test if table occupied by POS
                staffIdFrom = fromTable[8]
                staffIdTo = toTable[8]
                if (staffIdFrom != 0 and staffIdFrom is not None) or (staffIdTo != 0 and staffIdTo is not None):
                    self.sender.trigger('littlenanjing', 'App\\Events\\ChangeTableResult',
                                        {'staffId': data["staffId"], 'code': '-1',
                                         'message': '操作失败，该桌正被POS占用'})
                    return

                # check for table status first
                tableStatusFrom = fromTable[3]
                tableStatusTo = toTable[3]
                if tableStatusFrom != 2 and tableStatusTo != 0:
                    self.sender.trigger('littlenanjing', 'App\\Events\\ChangeTableResult',
                                        {'staffId': data["staffId"], 'code': '-2',
                                         'message': '只能换有人的桌去空桌！'})
                    return

                # check for salesorder status
                statusFrom = fromOrder[4]
                if statusFrom == 11:
                    self.sender.trigger('littlenanjing', 'App\\Events\\ChangeTableResult',
                                        {'staffId': data["staffId"], 'code': '-3',
                                         'message': '此桌订单显示已付款，不能换桌'})
                    return

                # swap the table contents
                posOperation.swapTable(fromTableCode, toTableCode)

                # update the given salesorder to given tableCode
                posOperation.updateSalesorderTableCode(fromOrder[0], toTableCode)

                # update any changes to Online before trigger event
                pollingDatabase.addTable(posOperation.getTableByTableCode(fromTableCode))
                pollingDatabase.addTable(posOperation.getTableByTableCode(toTableCode))
                pollingDatabase.findSalesOrder(toTableCode)

                self.sender.trigger('littlenanjing', 'App\\Events\\ChangeTableResult',
                                    {'staffId': data["staffId"], 'code': '0', 'message': 'success'})
        except:
            self.logger.exception("Exception Logged")

    def add_dish(self, data, *args, **kwargs):
        try:
            # print("processing Args:", args)
            # print("processing Kwargs:", kwargs)
            print("Channel Callback: %s" % data)
            print("Adding dishes")

            data = json.loads(data)
            tableCode = data["tableCode"]
            salesorderId = data["salesorderId"]
            salesorderLines = data["salesorderLines"]

            # test if this order/table is occupied at POS
            staffId = posOperation.getTableStaffId(tableCode)[0][0]
            if staffId != 0 and staffId is not None:
                self.sender.trigger('littlenanjing', 'App\\Events\\AddDishResult',
                                    {'staffId': data["staffId"], 'salesorderId': salesorderId, 'tableCode': tableCode,
                                     'code': '-1', 'message': 'Fail to add dish, table is using by POS'})
                return

            for item in salesorderLines:
                result = posOperation.insertSalesorderLine(item, salesorderId, data["staffId"])

                comments = item["comments"] or ""
                print("DISH: \n" +
                      "salesorderId, line_id, last_line_id\n {} added\n".format(
                          result))  # from the dish_line_id -> option_line_id

                # find printer and insert into kitchen
                posOperation.goToKitchen(result[1], comments)

            posOperation.updateSalesorderPrice(salesorderId)
            pollingDatabase.postSalesorderLine([salesorderId], comments)

            self.sender.trigger('littlenanjing', 'App\\Events\\AddDishResult',
                                {'staffId': data["staffId"], 'salesorderId': salesorderId, 'code': '0',
                                 'message': 'success'})
        except:
            self.logger.exception("Exception Logged")

    # We can't subscribe until we've connected, so we use a callback handler
    # to subscribe when able
    def connect_handler(self, data):
        channel = self.receiver.subscribe('littlenanjing')
        channel.bind('App\\Events\\OpenTableRequest', self.open_table)
        channel.bind('App\\Events\\AddDishRequest', self.add_dish)
        channel.bind('App\\Events\\ChangeTableRequest', self.change_table)
