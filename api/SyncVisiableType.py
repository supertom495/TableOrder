# -*- coding: utf-8 -*-
import os
import sys
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import yaml

from model import models

if not os.path.exists("./setting/flask.yaml"):
	print("did not found setting file")
	sys.exit()
with open('./setting/flask.yaml') as f:
	flaskConfig = yaml.load(f, Loader=yaml.FullLoader)
	if (len(flaskConfig) < 5): sys.exit()
serverName = flaskConfig.get("ServerName")
if serverName is None:
	serverName = socket.gethostbyname(socket.gethostname())


engine = create_engine('mssql+pymssql://{}:{}@{}/{}'.format(flaskConfig.get("Login"), flaskConfig.get("Password"), serverName, flaskConfig.get("DBName")), convert_unicode=True)  # 创建数据库引擎( 当前目录下保存数据库文件)

db_session = scoped_session(sessionmaker(autocommit=False,
										 autoflush=False,
										 bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

Base.metadata.create_all(bind=engine)

extraStock = models.ExtraStock.getAll()
tasteStock = models.TasteStock.getAll()

import pymssql

# conn = pymssql.connect('192.168.1.135', 'sa', '1689', 'gcvic', '1433')
conn = pymssql.connect('58.171.74.130', 'sa', 'AuPos122333', 'RPOSHEAD', port='11689')
"""
Extra
"""
cursor = conn.cursor()
cursor.execute('SELECT * FROM ExtraStock')
res = cursor.fetchall()

i = 0
recording = 0
size = len(res)
for row in res:
	i+=1
	percentage = int(((i)/size) * 100)
	if percentage > recording + 3:
		recording = percentage
		print( str(percentage) + '%')
	models.ExtraStock.updateVisibleType(row[0], row[1], row[2])

print('finish sync extra stock')

"""
Taste
"""
cursor = conn.cursor()
cursor.execute('SELECT * FROM TasteStock')
res = cursor.fetchall()

i = 0
recording = 0
size = len(res)
for row in res:
	i+=1
	percentage = int(((i)/size) * 100)
	if percentage > recording + 3:
		recording = percentage
		print( str(percentage) + '%')
	models.TasteStock.updateVisibleType(row[0], row[1], row[2])

print('finish sync taste stock')

"""
GlobalSetting
"""
cursor = conn.cursor()
cursor.execute('SELECT * FROM GlobalSetting WHERE setting_key like \'MenuOptionLimitation%\' or setting_key like \'MenuSizeLevelOptionDisallow%\'')
res = cursor.fetchall()

models.GlobalSetting.deleteAllRules()
for row in res:
	models.GlobalSetting.insertRules(row[0], row[1], row[2])


conn.close()
