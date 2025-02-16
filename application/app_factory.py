from flask import Flask
from application.config import config
from application.db.db_init import db
import os
import logging
import sys
from application.views.main_views import main


def create_app():
    app = Flask(__name__)

    config_name = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(
        config[config_name]()
    )  # Assuming config handles db URL and other settings

    # Initialize any app extensions, e.g., database
    db.init_app(app)
    app.logger.info("Database connection established")

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
