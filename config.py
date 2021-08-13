from os import path

# Getting app directory
BASE_DIR = path.dirname(path.abspath(__name__))


class Config:
    """
    Config class. Contains different config values.
    """

    DEBUG = True
    DATABASE_PATH = path.join(BASE_DIR, path.join('data', 'database.db'))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
