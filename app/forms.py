import string

from flask_wtf import Form
from wtforms import (
    TextField,
    PasswordField,
    BooleanField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import Required, Length, EqualTo, Email, Optional
from wtforms.widgets import PasswordInput

from app.lib.abstract import UserAbstraction


class LoginForm(Form):
    """ Login form with custom validate method """

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user_obj = None
        self.try_validate = False

    user_ident = TextField(
        'username', validators=[
            Required('E-mail/username field is required.'),
            Length(max=48, message='E-mail/username length must be '
                   'less than 48 chars.')]
    )
    password = PasswordField(
        'Password', validators=[
            Required('Password field is required.')],
        widget=PasswordInput()
    )
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')

    def validate_user_ident(form, *args, **kwargs):
        """ Validate user by provided username or email and password """

        user_mgr = UserAbstraction()
        user_ident = form.user_ident.data

        user_obj = None
        if "@" in user_ident:
            user_obj = user_mgr.get_by_email(user_ident)
        else:
            user_obj = user_mgr.get_by_username(user_ident)

        if user_obj and (user_mgr.check_password(user_obj, form.password.data)):
            form.user_obj = user_obj
            return True
        else:
            raise ValidationError('Couldn\'t find any user '
                                  'matching provided data')


class RegisterForm(Form):
    username = TextField(
        'username',
        validators=[Required('Username field is required.'),
                    Length(min=2, max=20, message='Username length'
                           'must be less than 20')]
    )

    email = TextField(
        'e-mail',
        validators=[Optional(), Email('Incorrect e-mail')])

    password = PasswordField(
        'password',
        validators=[Required('Password field is required'),
                    EqualTo('confirmpass', message='Passwords must match')]
    )

    confirmpass = PasswordField(
        'Confirm password',
        validators=[Required('Confirm your password'),
                    EqualTo('password', message='Passwords must match')]
    )

    submit = SubmitField('Confirm registration')

    def validate_username(form, field):
        if field.data:
            allowed_set = set(string.ascii_letters + string.digits + '_-')
            if set(field.data) - allowed_set:
                raise ValidationError('Username can contain only letters,'
                                      'digits, underscore and hyphen')
            user_mgr = UserAbstraction()
            if not user_mgr.get_by_username(field.data) is None:
                raise ValidationError('Such username already exists.')
            return True

    def validate_email(form, field):
        if field.data:
            user_mgr = UserAbstraction()
            if not user_mgr.get_by_email(field.data) is None:
                raise ValidationError('Such e-mail already exists.')
            return True
