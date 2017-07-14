import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET') or 'this-is-very-secret'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql://localhost/bucketlists'
    
class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bucketlists'
    DEBUG = True

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgres://dtxaabufzvgmsw:98322d762bb7e71aca19fd9c3cf552381bcabe4a4d23a62ab44011cdd39d5021@ec2-79-125-13-42.eu-west-1.compute.amazonaws.com:5432/d18m9d4h3p1s2c'

app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
