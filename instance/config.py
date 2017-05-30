import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('BLEED')
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'bucketlists.db')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}