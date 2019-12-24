import logging
import pysher
import sys
import pusher
import common
import json
import posOperation
import pollingDatabase
import threading

class PusherWebsocket:
    def __init__(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        ch = logging.StreamHandler(sys.stdout)
        root.addHandler(ch)


        self.receiver = pysher.Pusher(key=common.KEY, secure=common.SECURE, custom_host=common.HOST, port=common.PORT)
        self.sender = pusher.Pusher(app_id=common.APPID, key=common.KEY, secret=common.SECRET, ssl=common.SECURE, host=common.HOST, port=common.PORT)

        self.receiver.connection.bind('pusher:connection_established', self.connect_handler)
        self.receiver.connect()


    def open_table(self, data, *args, **kwargs):

        print("Channel Callback: %s" % data)
        print("Opening Table")
        data = json.loads(data)
        tableCode = data["tableCode"]
        guestNo = data["guestNo"]
        

        lock = threading.Lock()
        with lock:
            # test if table occupied by POS
            staffId = posOperation.getTableStaffId(tableCode)[0][0]
            if staffId != 0:
                self.sender.trigger('littlenanjing', 'App\\Events\\OpenTableResult', {'staffId': data["staffId"],'tableCode': tableCode, 'code': '-1', 'message':'Fail to open table, table is using by POS'})
                return

            # test if table is already opened
            tableStatus = posOperation.getTableByTableCode(tableCode)[0][3]
            if tableStatus != 0:
                self.sender.trigger('littlenanjing', 'App\\Events\\OpenTableResult', {'staffId': data["staffId"],'tableCode': tableCode, 'code': '-2', 'message':'Fail to open table, table is already opened'})
                return


            posOperation.activateTable(tableCode)
            salesorderId = posOperation.insertSalesorder(tableCode, guestNo, data["staffId"])
            
            table = posOperation.getTableByTableCode(tableCode)
            pollingDatabase.addTable(table)

            # send salesorder to api
            pollingDatabase.findSalesOrder(tableCode=tableCode)

            self.sender.trigger('littlenanjing', 'App\\Events\\OpenTableResult', {'staffId': data["staffId"],'tableCode': tableCode, 'code': '0', 'message':'success', 'salesorderId':salesorderId})


    def add_dish(self, data, *args, **kwargs):
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
        if staffId != 0:
            self.sender.trigger('littlenanjing', 'App\\Events\\AddDishResult', {'staffId': data["staffId"], 'salesorderId': salesorderId, 'tableCode': tableCode, 'code': '-1', 'message':'Fail to add dish, table is using by POS'})
            return



        for item in salesorderLines:
            result = posOperation.insertSalesorderLine(item, salesorderId, data["staffId"])
        
            comments = item["comments"]
            print("DISH: \n" + 
            "salesorderId, line_id, last_line_id\n {} added\n".format(result)) # from the dish_line_id -> option_line_id

            # find printer and insert into kitchen
            posOperation.goToKitchen(result[1], comments)

        pollingDatabase.postSalesorderLine([salesorderId], comments)
        
        self.sender.trigger('littlenanjing', 'App\\Events\\AddDishResult', {'staffId': data["staffId"],'salesorderId': salesorderId, 'code': '0', 'message':'success'})



    # We can't subscribe until we've connected, so we use a callback handler
    # to subscribe when able
    def connect_handler(self, data):
        channel = self.receiver.subscribe('littlenanjing')
        channel.bind('App\\Events\\OpenTableRequest', self.open_table)
        channel.bind('App\\Events\\AddDishRequest', self.add_dish)
