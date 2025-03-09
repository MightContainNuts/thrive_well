import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate


from flask_bootstrap import Bootstrap

from application.config import config
from application.views.main_views import main
from application.views.auth_views import auth
from application.views.user_views import user
from application.views.generate_views import gen
from application.views.chat_view import chat_bp
from application.db.models import User
from application.utils.extensions import mail, login_manager, db

base_dir = Path(__name__).parent.parent
MIGRATION_DIR = base_dir / "application" / "db" / "migrations"
load_dotenv()


login_manager.login_view = "auth.login"


def create_app():

    app = Flask(__name__)

    bootstrap = Bootstrap(app)
    assert bootstrap  # flake complains about unused variable'

    config_name = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config[config_name]())
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)

    migrate = Migrate(app, db, directory=str(MIGRATION_DIR))
    assert migrate  # flake complains about unused variable'

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
    app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL")
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    mail.init_app(app)

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
    app.register_blueprint(user, url_prefix="/user")
    app.register_blueprint(gen, url_prefix="/gen")
    app.register_blueprint(chat_bp, url_prefix="/chat")

    return app
