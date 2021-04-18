import os
import logging
from redis import Redis


class Config:
    APP_NAME = os.environ.get('APP_NAME', 'Demo App')
    SHORT_NAME = os.environ.get('SHORT_NAME', 'DemoApp')
    LOCATION = os.environ.get('LOCATION', 'Demo KPS')
    VERSION = 'v0.1'
    REFRESH_INTERVAL = int(os.environ.get('REFRESH_INTERVAL', 250))    # msec for page refresh

    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))

    LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)


class ProductionConfig(Config):
    DEBUG = False


class DebugConfig(Config):
    DEBUG = True


config = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}


# create logger
log = logging.getLogger()
log.setLevel(Config.LOG_LEVEL)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(Config.LOG_LEVEL)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
log.addHandler(ch)

# redis cache
cache = Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB)