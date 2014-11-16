import os

from app import app

class BaseConfig(object):
    BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    SECRET_KEY = '72f7cdbaae694f86bd7e219e8421a94d'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'bookshelf.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
    DEBUG = False
    
    APP_FOLDER = os.path.split(os.path.split(BASEDIR)[0])[0]
    TEMPLATES_FOLDER = os.path.join(APP_FOLDER, 'app', 'templates')

    USERDATA_DIRECTORY_NAME = "user_data"
    USERDATA_DIRECTORY = os.path.join(app.static_folder,
                                      USERDATA_DIRECTORY_NAME)
