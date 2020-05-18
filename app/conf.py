from os import getenv

class Config(object):
    DEBUG = False
    MONGO_URI = getenv('DB')
    CSRF_ENABLED = False
    GOOGLE_MAPS_API_TOKEN = getenv('GOOGLE_MAPS_API_TOKEN')