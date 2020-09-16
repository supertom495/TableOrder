# run.py
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_api import app
from flask_apscheduler import APScheduler
from apscheduler.triggers import interval
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from router.order import scanDeletedSalesorder, scanDeletedDocket

from database import getPort, init_db, flaskConfig

if flaskConfig.get('PiselUrl') is not None:
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    # scheduler = APScheduler(BackgroundScheduler(job_defaults=job_defaults, timezone=utc))
    # scheduler.init_app(app)
    # scheduler.start()

    scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone=utc)
    trigger1 = interval.IntervalTrigger(seconds=7)
    trigger2 = interval.IntervalTrigger(seconds=8)
    scheduler.add_job(scanDeletedSalesorder, trigger=trigger1, id='scanDeletedSalesorder', replace_existing=True)
    scheduler.add_job(scanDeletedDocket, trigger=trigger2, id='scanDeletedDocket', replace_existing=True)
    scheduler.start()



http_server = HTTPServer(WSGIContainer(app))
http_server.listen(getPort())
init_db()
IOLoop.instance().start()
