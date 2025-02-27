import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from application.config import config
from application.db_init import db
from application.views.main_views import main
from application.views.auth_views import auth

base_dir = Path(__name__).parent.parent
MIGRATION_DIR = base_dir / "application" / "db" / "migrations"
load_dotenv()


def create_app():

    app = Flask(__name__)

    config_name = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config[config_name]())
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    migrate = Migrate(app, db, directory=str(MIGRATION_DIR))
    assert migrate

    # Log the configuration
    app.logger.info(f"App started - Config name: {config_name}")
    app.logger.info(
        f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}"
    )  # noqa E501
    app.logger.info(f"FLASK_ENV: {os.environ.get('FLASK_ENV')}")
    app.logger.info(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")

    # Configure logging
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(app.config.get("LOG_LEVEL", logging.DEBUG))
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")

    return app
