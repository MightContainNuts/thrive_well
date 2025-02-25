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

base_dir = Path(__name__).parent.parent
MIGRATION_DIR = base_dir / "application" / "db" / "migrations"
load_dotenv()


def create_app():
    app = Flask(__name__)

    config_name = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(
        config[config_name]()
    )  # Assuming config handles db URL and other settings
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    # Initialize any app extensions, e.g., database
    db.init_app(app)
    migrate = Migrate(app, db, directory=str(MIGRATION_DIR))  # noqa E841
    with app.app_context():
        pass
        # db.create_all()

    app.logger.info(
        f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}"
    )  # noqa E501
    app.logger.info(f"FLASK_ENV: {os.environ.get('FLASK_ENV')}")
    app.logger.info(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
    app.logger.info(f"App started - Config name: {config_name}")

    # Configure logging
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(
        app.config.get("LOG_LEVEL", logging.DEBUG)
    )  # Default to DEBUG if not set in config

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    app.logger.info(f"App started - Config name: {config_name}")

    app.register_blueprint(main)  # Registering the main blueprint after config

    return app
