from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()
base_dir = Path(__name__).parent.parent


class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    # add local database


class TestConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": ProductionConfig,
}
