# run.py
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_api import app
from database import getPort

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(getPort())
IOLoop.instance().start()
