from os import getenv

class Config(object):
    DEBUG = False
    MONGO_URI = getenv('DB')
    CSRF_ENABLED = False