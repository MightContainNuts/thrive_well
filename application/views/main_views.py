from flask import Blueprint, session, redirect, url_for


main = Blueprint("main", __name__)


@main.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return f'user email: {session["user"]["email"]}'
