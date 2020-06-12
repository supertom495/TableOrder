import flask
from flask_cors import *
from database import init_db, db_session, getPort, debug
from router import blueprint
import time
import traceback
app = flask.Flask(__name__)
for item in blueprint: app.register_blueprint(item)
CORS(app, supports_credentials=True, resource=r'/*')


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.before_request
def logTime():
    app.logger.info("START: " + str(time.time()))


@app.after_request
def commit_session(response):
    db_session.commit()
    app.logger.info('RESPONSE - %s', response.data)
    app.logger.info("END  : " + str(time.time()))
    return response


@app.errorhandler(Exception)
def errorHandler(e):
    if app.config['DEBUG']:
        raise e
    else:
        db_session.rollback()
        app.logger.error(str(e) + "\n\n" + traceback.format_exc())
        return str(e) + "\n\n" + traceback.format_exc(), 500




if __name__ == '__main__':
    init_db()
    app.debug = debug
    port = getPort()

    import logging, logging.config, yaml
    logging.config.dictConfig(yaml.load(open('./setting/logging.yaml'), Loader=yaml.FullLoader))

    logfile = logging.getLogger('file')
    logconsole = logging.getLogger('console')
    logfile.debug("Debug FILE")
    logconsole.debug("Debug CONSOLE")

    app.run(host='0.0.0.0', port=port)
