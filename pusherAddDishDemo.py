import pysher
import sys
# Add a logging handler so we can see the raw communication data
import logging
import time
import pusher
import posOperation
import api
import common
import tableOrder
import json
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

receiver = pysher.Pusher("d422ef617a70042aa6b2", cluster="ap1", secure=True, secret="41e0bf31ef4a3b19b849")
sender = pusher.Pusher(app_id='623887', key='d422ef617a70042aa6b2', secret='41e0bf31ef4a3b19b849', cluster='ap1')

def add_dish(data, *args, **kwargs):
    print("processing Args:", args)
    print("processing Kwargs:", kwargs)
    print("Channel Callback: %s" % data)
    print("Table Opened")
    data = json.loads(data)

    salesorder_id = data["salesorderId"]
    stock_id = data["stockId"]
    quantity = data["quantity"]
    line_id = data["lineId"]
    parent_line_id = data["parentLineId"]
    line_type = data["lineType"]
    line_type = data["lineType"]

    common.setVar()
    posOperation.activateTable(tableCode)
    table = posOperation.getTableByTableCode(tableCode)
    tableOrder.addTable(table)
    
    sender.trigger('littlenanjing', 'App\\Events\\OpenTableResult', {'tableCode': tableCode,
        'code': '0', 'message':'giao'})
    # tableOrder.addTable(table)

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
    channel = receiver.subscribe('littlenanjing')
    channel.bind('App\\Events\\AddDishRequest', add_dish)

receiver.connection.bind('pusher:connection_established', connect_handler)
receiver.connect()


# sender - use this to call clould service
#----------------------------------------

#----------------------------------------

while True:
    # Do other things in the meantime here...
    time.sleep(1)
