# run.py
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_api import app
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

from database import getPort, init_db

# scheduler = apscheduler.schedulers.blocking.BackgroundScheduler('apscheduler.job_defaults.max_instances': '2')

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = APScheduler(BackgroundScheduler(job_defaults=job_defaults, timezone=utc))
# scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
scheduler.init_app(app)
scheduler.start()
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(getPort())
init_db()
IOLoop.instance().start()
