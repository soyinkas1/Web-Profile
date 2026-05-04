from flask import Flask, request
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from flask_bootstrap import Bootstrap
from flask_limiter import Limiter

from main_app.config import config


def _real_client_ip():
    """
    Return the real client IP, trusting PythonAnywhere's proxy headers.

    PythonAnywhere sits behind a reverse proxy, so request.remote_addr
    always points to the proxy — not the actual visitor. Without this,
    every request appears to come from the same IP and rate limiting
    would either block everyone or no one.
    """
    return (
        request.headers.get("X-Real-IP")
        or request.headers.get("X-Forwarded-For", request.remote_addr or "0.0.0.0")
                  .split(",")[0]
                  .strip()
    )


# Module-level extension instances (no app context yet)
mail = Mail()
db = SQLAlchemy()
flatpages = FlatPages()
freezer = Freezer()
bootstrap = Bootstrap()
limiter = Limiter(
    key_func=_real_client_ip,
    default_limits=["200 per day", "50 per hour"],
    strategy="fixed-window",
    headers_enabled=True,
)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialise Flask extensions with the application
    mail.init_app(app)
    db.init_app(app)
    flatpages.init_app(app)
    freezer.init_app(app)
    bootstrap.init_app(app)

    # Limiter is initialised AFTER config is loaded so it can read
    # RATELIMIT_STORAGE_URI
    limiter.init_app(app)

    # Register the blueprint
    from main_app.main import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
