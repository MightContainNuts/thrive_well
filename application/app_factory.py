from flask import Flask
from application.config import config
import os
from application.views.main_views import main
from application.logger import setup_logger


logger = setup_logger(__name__)


def create_app():
    app = Flask(__name__)
    config_name = os.environ.get("inst_config", "development")
    logger.info(f"Create new App instance using {config_name} configuration")
    config[config_name].init_app(app)
    app.register_blueprint(main)
    logger.info("Registering Blueprints")
    return app
