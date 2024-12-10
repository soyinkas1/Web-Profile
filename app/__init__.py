from flask import Flask, render_template
from flask_mail import Mail
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from flask_bootstrap import Bootstrap

# Create instances of the Flask extensions
mail = Mail()
db = SQLAlchemy()
flatpages = FlatPages()
freezer = Freezer()
bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initiate Flask extensions with the application
    mail.init_app(app)
    db.init_app(app)
    flatpages.init_app(app)
    freezer.init_app(app)
    bootstrap.init_app(app)

    # Register the blueprint
    from app.main import main_blueprint
    app.register_blueprint(main_blueprint)

   
    return app

