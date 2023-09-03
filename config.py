from os import getenv
from dotenv import dotenv_values
dot = dotenv_values()

class Config:
    SQLALCHEMY_ECHO = False
    DATABASE_URI = None 
    SECRET_KEY = None

class DevConfig(Config):
    ENV = 'DEV'
    DATABASE_URI = 'postgresql:///db_exercise_wtforms'
    SECRET_KEY = '123456_dev'

class TestConfig(Config):
    ENV = 'TEST'
    DATABASE_URI = 'sqlite://:memory:'
    SECRET_KEY = '123456_test'

class ProdConfig(Config):
    ENV = 'PROD'
    DATABASE_URI = getenv('DATABASE_URI', dot.get('DATABASE_URI'))
    SECRET_KEY = getenv('SECRET_KEY', dot.get('SECRET_KEY'))

class ExceptionMissingRunEnvironment(Exception):
    message = '--env variable is missing'

def get_config():
    """
        Get the app's configurations. Aware of ENV variable.
        ENV could be one of the following:
            "DEV", "TEST", "PROD"
    """
    env = getenv('ENV')
    if env == "DEV":
        return DevConfig
    elif env == "TEST":
        return TestConfig
    elif env == "PROD":
        return ProdConfig
    else:
        raise ExceptionMissingRunEnvironment()