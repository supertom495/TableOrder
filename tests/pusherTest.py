import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import requests
import json
import api
import common
import pusherWebsocket
import json
common.setVar()
common.setUpTable()
# common.setUpWebsocketServer()



pt = pusherWebsocket.PusherWebsocket()

data = json.dumps({
    "fromTableCode":"19",
    "toTableCode":"20",
    "staffId": 2
})

pt.change_table(data)