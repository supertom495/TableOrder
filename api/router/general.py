import flask
from utils import ServiceUtil, ResponseUtil
from model.BasicModel import GlobalSetting

general_blueprint = flask.Blueprint(
    'general',
    __name__,
    url_prefix='/api/v1/general'
)


@general_blueprint.route('/globalsetting', methods=['GET'])
def getGlobalSetting():
    # result = ServiceUtil.returnSuccess()

    settings = GlobalSetting.getOnlineSetting()
    data = {}
    for item in settings:
        key = item.setting_key.replace('Online_', '')
        value = item.setting_value
        data[key] = value

    result = ServiceUtil.returnSuccess(data)

    return ResponseUtil.success(result)
