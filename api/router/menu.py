import flask

menu_blueprint = flask.Blueprint(
    'menu',
    __name__,
    url_prefix='/api/menu'
)

@menu_blueprint.route('/keyboard')
def getKeyboard():
    return "a"


