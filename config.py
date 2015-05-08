import os
import logging

_this_directory = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    _filename = os.path.join(_this_directory,'.secret_key')

    try:
        SECRET_KEY = open(_filename,'rb').read()
    except IOError:
        print 'Error: No secret key. Create it with:'
        print 'head -c 24 /dev/urandom > %s' % (_filename)
        raise
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)s - %(funcName)s] %(message)s"

class DevConfig(Config):
    DEBUG = True
    TESTING = False
    LOG_FILENAME = os.path.join(_this_directory, 'logs/dev.log')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/dbs/dev.db' % _this_directory

class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    LOG_FILENAME = os.path.join(_this_directory, 'logs/prod.log')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/dbs/prod.db' % _this_directory
