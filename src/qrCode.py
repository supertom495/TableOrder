import api
import json
import qrcode



def getQrCode():
    result = json.loads(api.getToken().text)
    url = result["url"]
    print(url)
    img = qrcode.make(url)
    img.show(command='fim')

def refreshQrCode():
    result = json.loads(api.refreshToken().text)
    url = result["url"]
    print(url)
    img = qrcode.make(url)
    img.show(command='fim')