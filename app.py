
from flask import Flask, render_template, url_for, request

# from datetime import datetime
# import configparser
import os
# import re
import sys
from app import create_app, db, mail
from app.db_models import ContactTable
from flask_migrate import Migrate, init as flask_migrate_init, migrate as flask_migrate_migrate, upgrade as flask_migrate_upgrade
from dotenv import load_dotenv
from app.main.exception import CustomException
from app.main.logging import logging


# DEBUG = True
# FLATPAGES_AUTO_RELOAD = DEBUG
# FLATPAGES_EXTENSION = '.md'
# FLATPAGES_ROOT = 'content'
# DIR_BLOG_POSTS = 'blogs'
# DIR_PROJECTS = 'projects'


# app = Flask(__name__)
# flatpages = FlatPages(app)
# freezer = Freezer(app)





# Load environment variables
load_dotenv()

application = create_app(os.getenv('FLASK_CONFIG') or 'default')

app = application
migrate = Migrate(app, db)
logging.info('app created')
def make_shell_context():
    return dict(db=db, Contacts=ContactTable)

app.shell_context_processor(make_shell_context)
with app.app_context():
     # Initialize the migration repository if it doesn't exist
    migrations_path = os.path.join(os.path.dirname(__file__), 'migrations')
    if not os.path.exists(migrations_path):
        try:
            flask_migrate_init()
            logging.info("Migration repository initialized.")
        except Exception as e:
            raise CustomException(e, sys)
    
    # Run migrations
    try:
        # Generate an initial migration
        flask_migrate_migrate(message="Initial migration.")
        # Apply the migration to upgrade the database
        flask_migrate_upgrade()
        logging.info('Database upgraded successfuly')
    except Exception as e:
            raise CustomException(e, sys)

@app.cli.command()
def test():
    """Run the unit tests"""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)






app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)