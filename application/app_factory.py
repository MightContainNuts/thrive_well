from flask import Flask
from application.config import config
from application.views.main_views import main
from application.logger import setup_logger


logger = setup_logger(__name__)


def create_app(config_name):
    app = Flask(__name__)
    logger.info(f"Create new App instance using {config_name} configuration")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.register_blueprint(main)
    logger.info("Registering Blueprints")
    return app
