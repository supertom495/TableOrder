# import ftplib


# session = ftplib.FTP('server.address.com', 'USERNAME', 'PASSWORD')
# file = open('kitten.jpg', 'rb')                  # file to send
# session.storbinary('STOR kitten.jpg', file)     # send the file
# file.close()                                    # close file and FTP
# session.quit()

import ftplib
import os
import sys

# ftp = ftplib.FTP()
# host = "ftp.kidsnparty.com.au"
# port = 21
# ftp.connect(host, port)
# print(ftp.getwelcome())
# try:
#     print("Logging in...")

#     ftp.login("​admin@ozwearugg.com.au", "122333@Upos")
#     print("sss\n")

# with ftplib.FTP(host, '​admin@ozwearugg.com.au', '122333@Upos') as ftp, open("bi.png", 'rb') as file:
#     print(file)
#     print("sss\n")
#     ftp.cwd('/src/image')
#     ftp.storbinary('STOR kitten.jpg', file)

# except:
#     "failed to login"


def enter_dir(f, path):
    original_dir = f.pwd()
    try:
        f.cwd(path)
    except:
        return
    print(path)
    names = f.nlst()
    for name in names:
        enter_dir(f, path + '/' + name)
    f.cwd(original_dir)


f = ftplib.FTP()
host = "ftp.kidsnparty.com.au"
port = 21
f.connect(host, port)
print(f.getwelcome())

userName = "​admin@ozwearugg.com.au".strip(u'\u200b')
password = "122333@Upos".strip(u'\u200b')
fileName = "wallpaper_6.jpg"
# print(userName)

# f.login(userName.strip(u'\u200b'), password.strip(u'\u200b'))
# enter_dir(f, '/src/image')
with ftplib.FTP(host, userName, password) as ftp, open(fileName, 'rb') as file:

    ftp.cwd("/src/image/tableorder/bbqhot")
    ftp.storbinary("STOR %s" % fileName, file)
