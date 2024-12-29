import os

from dotenv import load_dotenv

load_dotenv(override=True)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
        SECRET_KEY = os.getenv('SECRET_KEY')
        MAIL_SERVER = os.getenv('MAIL_SERVER')
        MAIL_PORT = os.getenv('MAIL_PORT')
        MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
        MAIL_USERNAME = os.getenv('MAIL_USERNAME')
        MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
        DEV_DATABASE_URL = os.getenv('DEV_DATABASE_URL')
        DATABASE_URL = os.getenv('DATABASE_URL')
        SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
        FLASK_CONFIG = os.getenv('FLASK_CONFIG')
        MAIL_SUBJECT_PREFIX = os.getenv('MAIL_SUBJECT_PREFIX')
        DEBUG = os.getenv('DEBUG')
        FLATPAGES_AUTO_RELOAD = os.getenv('FLATPAGES_AUTO_RELOAD')
        FLATPAGES_EXTENSION = os.getenv('FLATPAGES_EXTENSION')
        FLATPAGES_ROOT = os.getenv('FLATPAGES_ROOT')
        DIR_BLOG_POSTS = os.getenv('DIR_BLOG_POSTS')
        DIR_PROJECTS = os.getenv('DIR_PROJECTS')
        DIR_TESTIMONIALS = os.getenv('DIR_TESTIMONIALS')
        DIR_TRAININGS = os.getenv('DIR_TRAININGS')
        


        @staticmethod
        def init_app(app):
                pass

class DevelopmentConfig(Config):
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
        SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
class TestingConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
        SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
class ProductionConfig(Config):
        DEBUG = False
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-production.sqlite')
        SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
        

config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}