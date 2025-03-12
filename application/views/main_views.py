from flask import Blueprint, render_template
from flask_login import current_user

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html", user=current_user)
