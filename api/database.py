# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import yaml
import os, sys
import pymssql

if not os.path.exists("./flask.yaml"):
	sys.exit()
with open('flask.yaml') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)
	if (len(data) != 5): sys.exit()

storeName = data.get("StoreName")
engine = create_engine('mssql+pymssql://{}:{}@{}/{}'.format(data.get("Login"), data.get("Password"), data.get("ServerName"), data.get("DBName")), convert_unicode=True)  # 创建数据库引擎( 当前目录下保存数据库文件)
db_session = scoped_session(sessionmaker(autocommit=False,
										 autoflush=False,
										 bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
# metadata = None

def init_db():
	# 在这里导入所有的可能与定义模型有关的模块，这样他们才会合适地
	# 在 metadata 中注册。否则，您将不得不在第一次执行 init_db() 时
	# 先导入他们。
	import models
	Base.metadata.create_all(bind=engine)
	# metadata = MetaData(engine)

