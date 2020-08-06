import flask
from flask_cors import *
from database import init_db, db_session, getPort, debug
from router import blueprint
import time, json
import traceback
app = flask.Flask(__name__)
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
        body = '[{}] \n {} \n\n'.format(time.asctime(time.localtime()), requestBody)
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

    import logging, logging.config, yaml
    logging.config.dictConfig(yaml.load(open('./setting/logging.yaml'), Loader=yaml.FullLoader))

    logfile = logging.getLogger('file')
    logconsole = logging.getLogger('console')
    logfile.debug("Debug FILE")
    logconsole.debug("Debug CONSOLE")


    app.run(host='0.0.0.0', port=port)
