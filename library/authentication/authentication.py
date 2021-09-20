from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps

from .services import *
from library.adapters.repository import repo_instance as repo

authentication_blueprint = Blueprint('authentication_bp', __name__)


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    not_unique = None

    if form.validate_on_submit():
        try:
            add_user(repo, form.user_name.data, form.password.data)
            return redirect(url_for('authentication_bp.login'))
        except NameNotUniqueException:
            not_unique = "This username is already taken. Please choose a different one."

    return render_template(
        'authentication/credentials.html',
        title='Register',
        form=form,
        error_message=not_unique,
        handler_url=url_for('authentication_bp.register')
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_message = None

    if form.validate_on_submit():
        try:
            user = get_user(repo, form.user_name.data)

            authenticate_user(repo, user["user_name"], form.password.data)

            session.clear()
            session["user_name"] = user["user_name"]
            return redirect(url_for('home_bp.home'))
        except (UnknownUserException, AuthenticationException):
            error_message = "Invalid username or password."

    return render_template(
        'authentication/credentials.html',
        title='Login',
        error_message=error_message,
        form=form
    )


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain at least one upper case letter,\
            one lower case letter and one digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('Username:', [
        DataRequired(message='Your username is required'),
        Length(min=3, message='Your username is too short')])
    password = PasswordField('Password:', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_name = StringField('Username:', [
        DataRequired()])
    password = PasswordField('Password:', [
        DataRequired()])
    submit = SubmitField('Login')
