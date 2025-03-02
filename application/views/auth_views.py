from flask import Blueprint, render_template
from flask_login import login_user, logout_user, login_required
from application.forms import LoginForm, RegistrationForm

from application.db.models import User, Profile

from flask import flash, redirect, request, url_for
from application.db_init import db


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("Invalid username or password.")

    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            user_name=form.username.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()


        profile = Profile(
            user_id=user.user_id,  # Link profile to user via user_id
            user_name=form.username.data,
        )
        db.session.add(profile)
        db.session.commit()  # Commit to generate profile_id


        flash("You can now login.")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)
