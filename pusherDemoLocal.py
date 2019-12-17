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

receiver = pysher.Pusher(key="ABCDEF", secure=False, custom_host="192.168.1.26", port="6001")
sender = pusher.Pusher(app_id='12345', key='ABCDEF', secret='HIJKLMNOP', ssl=False, host='192.168.1.26', port=6001)

def open_table(data, *args, **kwargs):
    print("processing Args:", args)
    print("processing Kwargs:", kwargs)
    print("Channel Callback: %s" % data)
    print("Table Opened")
    data = json.loads(data)
    tableCode = data["tableCode"]
    common.setVar()
    posOperation.activateTable(tableCode)
    table = posOperation.getTableByTableCode(tableCode)
    tableOrder.addTable(table)
    sender.trigger('littlenanjing', 'App\\Events\\OpenTableResult', {'tableCode': tableCode,
        'code': '0', 'message':'giao', 'salesorderId':1234})
    tableOrder.addTable(table)

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
    channel = receiver.subscribe('littlenanjing')
    channel.bind('App\\Events\\OpenTableRequest', open_table)

receiver.connection.bind('pusher:connection_established', connect_handler)
receiver.connect()


# sender - use this to call clould service
#----------------------------------------

#----------------------------------------

while True:
    # Do other things in the meantime here...
    time.sleep(1)
