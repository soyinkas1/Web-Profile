import os

from dotenv import load_dotenv

load_dotenv(override=True)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
        SECRET_KEY = os.getenv('MAIN_SECRET_KEY')
        MAIL_SERVER = os.getenv('MAIN_MAIL_SERVER')
        MAIL_PORT = os.getenv('MAIN_MAIL_PORT')
        MAIL_USE_TLS = os.getenv('MAIN_MAIL_USE_TLS')
        MAIL_USERNAME = os.getenv('MAIN_MAIL_USERNAME')
        MAIL_PASSWORD = os.getenv('MAIN_MAIL_PASSWORD')
        DEV_DATABASE_URL = os.getenv('MAIN_DEV_DATABASE_URL')
        DATABASE_URL = os.getenv('MAIN_DATABASE_URL')
        SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('MAIN_SQLALCHEMY_TRACK_MODIFICATIONS')
        FLASK_CONFIG = os.getenv('MAIN_FLASK_CONFIG')
        MAIL_SUBJECT_PREFIX = os.getenv('MAIN_MAIL_SUBJECT_PREFIX')
        DEBUG = os.getenv('MAIN_DEBUG')
        FLATPAGES_AUTO_RELOAD = os.getenv('MAIN_FLATPAGES_AUTO_RELOAD')
        FLATPAGES_EXTENSION = os.getenv('MAIN_FLATPAGES_EXTENSION')
        FLATPAGES_ROOT = os.getenv('MAIN_FLATPAGES_ROOT')
        DIR_BLOG_POSTS = os.getenv('MAIN_DIR_BLOG_POSTS')
        DIR_PROJECTS = os.getenv('MAIN_DIR_PROJECTS')
        DIR_TESTIMONIALS = os.getenv('MAIN_DIR_TESTIMONIALS')
        DIR_TRAININGS = os.getenv('MAIN_DIR_TRAININGS')
        


        @staticmethod
        def init_app(app):
                pass

class DevelopmentConfig(Config):
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = os.environ.get('MAIN_DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
        SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('MAIN_SQLALCHEMY_TRACK_MODIFICATIONS')
class TestingConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = os.environ.get('MAIN_TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
        SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('MAIN_SQLALCHEMY_TRACK_MODIFICATIONS')
        WTF_CSRF_ENABLED = False
        MAIL_SUPPRESS_SEND = True # Do not send emails during tests 
        MAIL_DEBUG = int(os.getenv('MAIL_DEBUG', 0))
        FLATPAGES_EXTENSION = '.md' 
        FLATPAGES_ROOT = os.path.join(basedir, 'content')
class ProductionConfig(Config):
        DEBUG = False
        SQLALCHEMY_DATABASE_URI = os.environ.get('MAIN_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-production.sqlite')
        SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('MAIN_SQLALCHEMY_TRACK_MODIFICATIONS')
        

config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}