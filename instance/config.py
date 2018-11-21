# /instance/config.py

import os

class Config(object):
    """Parent configuration class."""
    DEBUG = True
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

POSTGRES = {
    'user': 'postgres',
    'pw': '',
    'db': 'send_it',
    'host': 'localhost',
    'port': '5432',
}


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    use_reloader=True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}