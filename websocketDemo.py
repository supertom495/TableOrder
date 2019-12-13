import pysher
import sys
# Add a logging handler so we can see the raw communication data
import logging
import time

root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

pusher = pysher.Pusher("d422ef617a70042aa6b2", cluster="ap1", secure=True, secret="41e0bf31ef4a3b19b849")


def  my_func(*args, **kwargs):
    print("processing Args:", args)
    print("processing Kwargs:", kwargs)

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
    channel = pusher.subscribe('posts.10')
    channel.bind('ChangTableStatus', my_func)

pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()



while True:
    # Do other things in the meantime here...
    time.sleep(1)