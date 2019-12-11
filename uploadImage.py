import ftplib
import os
import sys
import posOperation
import common


common.setVar()  # FIXME delete this line
f = ftplib.FTP()
host = "ftp.kidsnparty.com.au"
port = 21
f.connect(host, port)
print(f.getwelcome())

userName = "​admin@ozwearugg.com.au".strip(u'\u200b')
password = "122333@Upos".strip(u'\u200b')

stockList = posOperation.getStockBarcode()
pictureList = []

for stock in stockList:
    barcode = stock[0]
    filePath = common.PICTUREPATH + barcode + ".jpg"

    if os.path.exists(filePath):
        pictureList.append(filePath)


with ftplib.FTP(host, userName, password) as ftp:
    ftp.cwd("/src/image/tableorder/bbqhot")

    for picture in pictureList:
        with open(picture, 'rb') as file:
            ftp.storbinary("STOR %s" % picture.split("/")[-1], file)
