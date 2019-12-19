import pysher
import sys
import time

# Add a logging handler so we can see the raw communication data
import logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

global pusher

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
    channel = pusher.subscribe('live_trades')
    channel.bind('trade', callback)

appkey = "de504dc5763aeef9ff52"
pusher = pysher.Pusher(appkey)
pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

print("finished")

while True:
    time.sleep(1)