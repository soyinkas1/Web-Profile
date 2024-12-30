from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()
