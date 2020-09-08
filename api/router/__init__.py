from router.menu import menu_blueprint
from router.staff import staff_blueprint
from router.order import order_blueprint
from router.raw import raw_blueprint
from router.report import report_blueprint
from router.tyro import tyro_blueprint

blueprint = [
    menu_blueprint,
    staff_blueprint,
    order_blueprint,
    raw_blueprint,
    report_blueprint,
    tyro_blueprint
]