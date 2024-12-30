from flask import Blueprint

demo1_app = Blueprint('demo1_app', __name__, static_folder='static', template_folder='templates')

from . import views

