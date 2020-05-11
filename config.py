import os

from app.database.postgresql import postgresql_uri

BASE_DIR = os.getcwd()
# MODULE_DIR = os.path.join(os.getcwd(), 'app/modules/')
LOG_DIR = os.path.join(os.getcwd(), 'logs/')

class Config(object):
    JSON_AS_ASCII = False
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    # postgresql
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = postgresql_uri