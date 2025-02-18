import os

from dotenv import load_dotenv

load_dotenv(dotenv_path='demo_app1_app/app/.env', override=True)  
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
class Config:
        SECRET_KEY = os.getenv('DEMO1_SECRET_KEY')
        MAIL_SERVER = os.getenv('DEMO1_MAIL_SERVER')
        MAIL_PORT = os.getenv('DEMO1_MAIL_PORT')
        MAIL_USE_TLS = os.getenv('DEMO1_MAIL_USE_TLS')
        MAIL_USERNAME = os.getenv('DEMO1_MAIL_USERNAME')
        MAIL_PASSWORD = os.getenv('DEMO1_MAIL_PASSWORD')
        MAIL_SUBJECT_PREFIX = os.getenv('DEMO1_MAIL_SUBJECT_PREFIX')
        DEV_DATABASE_URL = os.getenv('DEMO1_DEV_DATABASE_URL')
        DATABASE_URL = os.getenv('DEMO1_DATABASE_URL')
        


        @staticmethod
        def init_app(app):
                pass


class DevelopmentConfig(Config):
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = os.environ.get('DEMO1_DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'demo_app1-dev.sqlite')
        SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('DEMO1_SQLALCHEMY_TRACK_MODIFICATIONS')
class TestingConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'demo_app1-test.sqlite')
        SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('DEMO1_SQLALCHEMY_TRACK_MODIFICATIONS')
        WTF_CSRF_ENABLED = False
        MAIL_SUPPRESS_SEND = True # Do not send emails during tests 
        MAIL_DEBUG = int(os.getenv('MAIL_DEBUG', 0))
        FLATPAGES_EXTENSION = '.md' 
        FLATPAGES_ROOT = os.path.join(basedir, 'content')
class ProductionConfig(Config):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'demo_app1-test.sqlite')
        SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('DEMO1_SQLALCHEMY_TRACK_MODIFICATIONS')
        

config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}