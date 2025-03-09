from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


mail = Mail()
login_manager = LoginManager()
db = SQLAlchemy()
