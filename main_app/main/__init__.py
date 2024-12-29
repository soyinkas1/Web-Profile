from flask import Blueprint

main_blueprint = Blueprint('main', __name__, static_folder='static', template_folder='templates')

from . import views, errors