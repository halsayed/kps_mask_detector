import os
import logging
from redis import Redis


class Config:

    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))

    NATS_HOST = os.environ.get('NATS_HOST', 'nats')
    NATS_PORT = int(os.environ.get('NATS_PORT', '4222'))
    NATS_SUBJECT = os.environ.get('NATS_SUBJECT', 'KPS')

    LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)


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