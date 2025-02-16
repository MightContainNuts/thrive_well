from pathlib import Path
import os

base_dir = Path(__name__).parent.parent


class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # add local database


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class ProductionConfig(Config):
    DEBUG = True
    # Handle the URI modification for production
    uri = os.getenv("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri


config = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": ProductionConfig,
}
