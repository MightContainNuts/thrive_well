from pathlib import Path
import os

base_dir = Path(__name__).parent.parent


class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # add local database


class TestConfig(Config):
    DEBUG = True
    # add local database


class ProductionConfig(Config):
    DEBUG = True
    # add remote db


config = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": ProductionConfig,
}
