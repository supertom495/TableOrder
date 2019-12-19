import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import pysher
# Add a logging handler so we can see the raw communication data
import logging
import time
import pusher
import posOperation
import api
import common
import TableOrder
import json
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

# receiver = pysher.Pusher("d422ef617a70042aa6b2", cluster="ap1", secure=True, secret="41e0bf31ef4a3b19b849")
# sender = pusher.Pusher(app_id='623887', key='d422ef617a70042aa6b2', secret='41e0bf31ef4a3b19b849', cluster='ap1')

receiver = pysher.Pusher(key="ABCDEF", secure=False, custom_host="192.168.1.26", port="6001")
sender = pusher.Pusher(app_id='12345', key='ABCDEF', secret='HIJKLMNOP', ssl=False, host='192.168.1.26', port=6001)

def add_dish(data, *args, **kwargs):
    print("processing Args:", args)
    print("processing Kwargs:", kwargs)
    print("Channel Callback: %s" % data)
    print("Table Opened")
    with open(r"salesorderLine.json", 'r') as f:
        data = json.load(f)

    salesorderId = data["salesorderId"]
    salesorderLines = data["salesorderLines"]
    for salesorderLine in salesorderLines:
        stockId = salesorderLine["stockId"]
        quantity = salesorderLine["quantity"]
        stockTaste = salesorderLine["stockTaste"]
        stockExtra = salesorderLine["stockExtra"]
        comments = salesorderLine["comments"]


    common.setVar()

    TableOrder.addTable()
    
    sender.trigger('littlenanjing', 'App\\Events\\AddDishResult', {'salesorderId': 1234,
        'code': '0', 'message':'success'})


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
