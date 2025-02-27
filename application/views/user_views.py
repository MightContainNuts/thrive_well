from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

user = Blueprint("user", __name__)


@user.route("/profile")
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    # You can now directly access current_user in the template
    return render_template("profile.html", user=current_user)
