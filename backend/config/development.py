from .default import Config


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False