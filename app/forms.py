import string

from flask_wtf import Form
from wtforms import (
    TextField,
    PasswordField,
    BooleanField,
    FieldList,
    HiddenField,
    FormField,
    SubmitField,
    SelectMultipleField,
    ValidationError,
)
from wtforms.validators import Required, Length, EqualTo, Email
from wtforms.widgets import PasswordInput

from app.lib.abstract import UserAbstraction


REQUIRED_FIELD = '%s field is required'
LENGTH_FIELD = '%s length must be less than %d'


class LoginForm(Form):
    """ Login form """

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user_obj = None
        self.try_validate = False

    user_ident = TextField(
        'userident', validators=[
            Required(REQUIRED_FIELD % 'E-mail/username'),
            Length(max=48, message=LENGTH_FIELD % ('E-mail/username', 48))]
    )
    password = PasswordField(
        'Password', validators=[
            Required(REQUIRED_FIELD % 'Password')],
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
        'Username',
        validators=[Required(REQUIRED_FIELD % 'Username'),
                    Length(min=2, max=20, message=LENGTH_FIELD %
                           ('Username', 20))]
    )

    email = TextField(
        'E-mail',
        validators=[Required(REQUIRED_FIELD % 'E-mail'),
                    Email('Incorrect e-mail')])

    password = PasswordField(
        'Password',
        validators=[Required(REQUIRED_FIELD % 'Password'),
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


class AddBookForm(Form):
    new_book = TextField(
        'Title',
        validators=[Required(REQUIRED_FIELD % 'Title'),
                    Length(max=50, message=LENGTH_FIELD % ('Title', 50))]
    )
    authors = SelectMultipleField('authors')
    submit = SubmitField('Add book')


class AddAuthorForm(Form):
    new_author = TextField(
        'Name',
        validators=[Required(REQUIRED_FIELD % 'Name'),
                    Length(max=50, message=LENGTH_FIELD % ('Name', 50))]
    )
    books = SelectMultipleField('books')
    submit = SubmitField('Add author')


class BookForm(Form):
    book_id = HiddenField('book_id')
    title = TextField('title')
    authors = FieldList(TextField('name'))
    edit = SubmitField('edit')
    delete = SubmitField('delete')


class BookListForm(Form):
    books = FieldList(FormField(BookForm))


class AuthorForm(Form):
    author_id = HiddenField('author_id')
    name = TextField('name')
    books = FieldList(TextField('title'))
    edit = SubmitField('edit')
    delete = SubmitField('delete')


class AuthorListForm(Form):
    authors = FieldList(FormField(AuthorForm))
