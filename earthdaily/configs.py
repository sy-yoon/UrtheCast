import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    """Flask Config"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1qaz2wsx!!@ec2-54-215-238-23.us-west-1.compute.amazonaws.com:5432/postgres'
    SWAGGER_UI_DOC_EXPANSION = 'list'

    def __init__(self):
        db_env = os.environ.get('SQLALCHEMY_DATABASE_URI')
        if db_env:
            self.SQLALCHEMY_DATABASE_URI = db_env

class DevelopmentConfig(Config):
    """Flask Config for Dev"""
    DEBUG=True

class TestingConfig(DevelopmentConfig):
    __test__ = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1qaz2wsx!!@localhost:5432/postgres'

class ProductionConfig(Config):
    """Flask Config for Production"""
    pass