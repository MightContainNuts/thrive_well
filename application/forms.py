from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

from application.db.models import User


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(1, 64)]
    )  # noqa E501
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(1, 64)]
    )  # noqa E501
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, numbers, dots or underscores",  # noqa E501
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(8, 64),
            EqualTo("password2", "Passwords must match"),
        ],
    )
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")

    def validate_username(self, field):
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError("Username already in use.")
