# -*- coding: utf-8 -*-
import importlib
import os
import sys
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import yaml

if not os.path.exists("./setting/flask.yaml"):
	print("did not found setting file")
	sys.exit()
with open('./setting/flask.yaml') as f:
	flaskConfig = yaml.load(f, Loader=yaml.FullLoader)
	if (len(flaskConfig) < 5): sys.exit()


def getPort():
	if os.path.exists("./setting/port.yaml"):
		with open('./setting/port.yaml') as f:
			file = yaml.load(f, Loader=yaml.FullLoader)
			port = file.get("port")
			return port
	else: return 5001


storeName = flaskConfig.get("StoreName")
serverName = flaskConfig.get("ServerName")
if serverName is None:
	serverName = socket.gethostbyname(socket.gethostname())
debug = flaskConfig.get("Debug")
engine = create_engine('mssql+pymssql://{}:{}@{}/{}'.format(flaskConfig.get("Login"), flaskConfig.get("Password"), serverName, flaskConfig.get("DBName")), convert_unicode=True)  # 创建数据库引擎( 当前目录下保存数据库文件)
db_session = scoped_session(sessionmaker(autocommit=False,
										 autoflush=False,
										 bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
# metadata = None

def init_db():
	"""
    在这里导入所有的可能与定义模型有关的模块，这样他们才会合适地
    在 metadata 中注册。否则，您将不得不在第一次执行 init_db() 时
    先导入他们。
 	"""
	# Added to models.tables the new table I needed ( format Table as written above )
	table_models = importlib.import_module('models')

	if not engine.dialect.has_table(engine, 'SalesOrderOnline', schema = 'dbo'):
		# Grab the class that represents the new table
		ORMTable = getattr(table_models, 'SalesorderOnline')

		# checkfirst=True to make sure it doesn't exists
		ORMTable.__table__.create(bind=engine, checkfirst=True)

	if not engine.dialect.has_table(engine, 'SalesOrderLineOnline', schema = 'dbo'):
		ORMTable = getattr(table_models, 'SalesorderLineOnline')
		ORMTable.__table__.create(bind=engine, checkfirst=True)
	if not engine.dialect.has_table(engine, 'DocketOnline', schema = 'dbo'):
		ORMTable = getattr(table_models, 'DocketOnline')
		ORMTable.__table__.create(bind=engine, checkfirst=True)
	if not engine.dialect.has_table(engine, 'RecordedDate', schema = 'dbo'):
		ORMTable = getattr(table_models, 'RecordedDate')
		ORMTable.__table__.create(bind=engine, checkfirst=True)

	Base.metadata.create_all(bind=engine)
	# metadata = MetaData(engine)

