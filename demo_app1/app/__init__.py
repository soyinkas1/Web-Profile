from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from demo_app1.config import config
from .main import demo1_app
from .extensions import db2, mail, bootstrap
# Create instances of the Flask extensions
# bootstrap = Bootstrap()
# mail = Mail()
# db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initiate Flask extensions with the application
    bootstrap.init_app(app)
    mail.init_app(app)
    
    db2.init_app(app)
    # app.register_blueprint(demo1_app, url_prefix='/demo1')

    return app

