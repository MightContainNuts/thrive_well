import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth

from application.config import config
from application.db_init import db
from application.views.main_views import main
from application.views.auth_views import auth_views

base_dir = Path(__name__).parent.parent
MIGRATION_DIR = base_dir / "application" / "db" / "migrations"
load_dotenv()


def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # Load the config before initializing OAuth or other extensions
    config_name = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(
        config[config_name]()
    )  # Assuming config handles db URL and other settings
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID")
    app.config["GOOGLE_CLIENT_SECRET"] = os.getenv("GOOGLE_CLIENT_SECRET")
    app.config["REDIRECT_URI"] = os.getenv(
        "REDIRECT_URI", "http://localhost:5000/auth/oauth-authorized"
    )
    # Set the secret key

    # Initialize the OAuth extension with the app
    oauth = OAuth(app)
    google = oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        authorize_params={"scope": "openid email profile"},
        access_token_url="https://accounts.google.com/o/oauth2/token",
        access_token_params=None,
        client_kwargs={"scope": "openid email profile"},
        api_base_url="https://www.googleapis.com/oauth2/v1/",
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    )

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
    app.register_blueprint(
        auth_views(google), url_prefix="/auth"
    )  # Registering the auth views blueprint

    return app
