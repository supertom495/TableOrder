import flask
from flask_cors import *
from database import init_db, db_session, getPort, debug, flaskConfig
from router import blueprint
import time, json
import traceback

class Config(object):  # 创建配置，用类
    # 任务列表
    JOBS = [
        # {  # 第一个任务
        #     'id': 'job1',
        #     'func': '__main__:job_1',
        #     'args': (1, 2),
        #     'trigger': 'cron', # cron表示定时任务
        #     'hour': 19,
        #     'minute': 27
        # },
        {  # 第1个任务，每隔6S执行一次
            'id': 'job1',
            'func': 'router.order:scanDeletedSalesorder',  # 方法名
            'args': (),  # 入参
            'trigger': 'interval',  # interval表示循环任务
            'seconds': 6,
        },
        {  # 第二个任务，每隔7S执行一次
            'id': 'job2',
            'func': 'router.order:scanDeletedDocket', # 方法名
            'args': (), # 入参
            'trigger': 'interval', # interval表示循环任务
            'seconds': 7,
        }
    ]


app = flask.Flask(__name__)
app.config.from_object(Config())  # 为实例化的flask引入配置
for item in blueprint: app.register_blueprint(item)
CORS(app, supports_credentials=True, resource=r'/*')


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.after_request
def commit_session(response):
    if response.status_code == 200:
        db_session.commit()
    else:
        db_session.rollback()

        requestBody = json.dumps(flask.request.values.dicts[1].to_dict(flat=False))
        responseBody = json.dumps(response.json)
        msg = requestBody + '\n' + responseBody
        body = '[{}] \n {} \n\n'.format(time.asctime(time.localtime()), msg)
        app.logger.error(body)

    return response


@app.errorhandler(Exception)
def errorHandler(e):

    if app.config['DEBUG']:
        raise e
    else:
        error = '[{}] \n{} \n'.format(time.asctime(time.localtime()), traceback.format_exc())
        app.logger.error(error)
        return 'error', 500



if __name__ == '__main__':
    init_db()
    app.debug = debug
    port = getPort()
    app.run(host='0.0.0.0', port=port)

    import logging, logging.config, yaml
    logging.config.dictConfig(yaml.load(open('./setting/logging.yaml'), Loader=yaml.FullLoader))

    logfile = logging.getLogger('file')
    logconsole = logging.getLogger('console')
    logfile.debug("Debug FILE")
    logconsole.debug("Debug CONSOLE")


