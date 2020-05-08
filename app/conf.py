from os import environ

class Config(object):
    DEBUG = False

    MONGO_URI = environ['DB']
    CSRF_ENABLED = False