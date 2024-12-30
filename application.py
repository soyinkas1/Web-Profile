
# from flask import Flask, render_template, url_for, request

# # from datetime import datetime
# # import configparser
# import os
# # import re
# import sys
# from main_app import create_app, db, mail
# from main_app.db_models import ContactTable
# from flask_migrate import Migrate, init as flask_migrate_init, migrate as flask_migrate_migrate, upgrade as flask_migrate_upgrade
# from dotenv import load_dotenv
# from main_app.main.exception import CustomException
# from main_app.main.logging import logging

# # Load environment variables
# load_dotenv()

# application = create_app(os.getenv('FLASK_CONFIG') or 'default')

# app = application
# migrate = Migrate(app, db)
# logging.info('app created')
# def make_shell_context():
#     return dict(db=db, Contacts=ContactTable)

# app.shell_context_processor(make_shell_context)
# with app.app_context():
#      # Initialize the migration repository if it doesn't exist
#     migrations_path = os.path.join(os.path.dirname(__file__), 'migrations')
#     if not os.path.exists(migrations_path):
#         try:
#             flask_migrate_init()
#             logging.info("Migration repository initialized.")
#         except Exception as e:
#             raise CustomException(e, sys)
    
#     # Run migrations
#     try:
#         # Generate an initial migration
#         flask_migrate_migrate(message="Initial migration.")
#         # Apply the migration to upgrade the database
#         flask_migrate_upgrade()
#         logging.info('Database upgraded successfuly')
#     except Exception as e:
#             raise CustomException(e, sys)

# @app.cli.command()
# def test():
#     """Run the unit tests"""
#     import unittest

#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)



# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000)






# app = Flask(__name__)

# @app.route('/')
# def homepage():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, url_for, request
import os
import sys
from main_app import create_app as create_main_app, db as main_db, mail as main_mail
from main_app.db_models import ContactTable as MainContactTable
from demo_app1.app import create_app as create_demo1_app, db as demo1_db, mail as demo1_mail
from demo_app1.app.db_models import HeartPredictions as Demo1Table
from flask_migrate import Migrate, init as flask_migrate_init, migrate as flask_migrate_migrate, upgrade as flask_migrate_upgrade
from dotenv import load_dotenv
from main_app.main.exception import CustomException
from main_app.main.logging import logging
from demo_app1.app.main import demo1_app

# Load environment variables for both apps
load_dotenv(dotenv_path='main_app/.env')   
load_dotenv(dotenv_path='demo_app1_app/app/.env')  
    
# Create the main and demo apps
main_app = create_main_app(os.getenv('MAIN_FLASK_CONFIG') or 'default')
demo_app = create_demo1_app(os.getenv('DEMO1_FLASK_CONFIG') or 'default')

# Register the demo app as a Blueprint within the main app
main_app.register_blueprint(demo1_app, url_prefix='/demo1')

app = main_app  # Set the main app as the primary application

# Configure migrations for both databases
migrate_main = Migrate(main_app, main_db)
migrate_demo1 = Migrate(demo_app, demo1_db)

logging.info('Main app and demo1 app created')

# Define shell context for main app
def make_main_shell_context():
    return dict(db=main_db, Contacts=MainContactTable)

# Define shell context for demo app
def make_demo1_shell_context():
    return dict(db=demo1_db, Predictions=Demo1Table)

main_app.shell_context_processor(make_main_shell_context)
demo_app.shell_context_processor(make_demo1_shell_context)

# Initialize and migrate databases for both apps
def initialize_and_migrate(app, db, migrate, migrations_subfolder):
    """
    Initialize and migrate the database for a specific app.
    
    Args:
        app: Flask app instance.
        db: SQLAlchemy database instance.
        migrate: Flask-Migrate instance.
        migrations_subfolder: Subfolder name for the app's migrations directory.
    """
    with app.app_context():
        migrations_path = os.path.join(os.path.dirname(__file__), migrations_subfolder)
        if not os.path.exists(migrations_path):
            try:
                flask_migrate_init(directory=migrations_subfolder)
                logging.info(f"Migration repository initialized for {app.name} at {migrations_subfolder}..")
            except Exception as e:
                raise CustomException(e, sys)
        try:
            flask_migrate_migrate(directory=migrations_subfolder, message="Initial migration.")
            flask_migrate_upgrade(directory=migrations_subfolder)
            logging.info(f'Database upgraded successfully for {app.name}.')
        except Exception as e:
            logging.error(f"Error during migration for {app.name}: {e}")
            raise CustomException(e, sys)

main_migrations_subfolder = "migrations/main_app"
demo1_app_migrations_subfolder = "migrations/demo1_app"
initialize_and_migrate(main_app, main_db, migrate_main, migrations_subfolder=main_migrations_subfolder )
initialize_and_migrate(demo_app, demo1_db, migrate_demo1, migrations_subfolder=demo1_app_migrations_subfolder)

@app.cli.command()
def test():
    """Run the unit tests"""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

application= main_app
if __name__ == '__main__':
    main_app.run(debug=True)