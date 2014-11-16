from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exc

from app.db import db_session
from app.lib import errors
from app import models


class BaseDBAbstraction(object):
    """ Base class for other abstractions """

    model = None

    def __init__(self, session=None):
        self.created_session = False

        if session:
            self.session = session
        else:
            self.session = self._create_session()
            self.created_session = True

    def _create_session(self):
        return db_session

    def save(self):
        self.session.commit()

    def revert(self):
        self.session.rollback()

    def safe_execute(self, method=None, *args, **kwargs):
        on_success = kwargs.pop('on_success', self.save)
        on_failure = kwargs.pop('on_failure', self.revert)

        try:
            if method:
                res = method(*args, **kwargs)
                on_success()
                return res
            on_success()

        except exc.IntegrityError, err:
            on_failure()
            message = err.message

            raise errors.DBRecordExists(message)


class UserAbstraction(BaseDBAbstraction):
    """ Abstraction for User model """

    model = models.User

    def create(self, *args, **kwargs):
        return self.safe_execute(self._create, *args, **kwargs)

    def _create(self, *args, **kwargs):
        new_user = self.model()

        new_user.username = kwargs.get('username', '')
        new_user.email = kwargs.get('email', '')

        password = kwargs.get('password')
        new_user.password = self.set_password(password)

        self.session.add(new_user)

        return new_user

    def set_password(self, raw_password):
        """ Create hashed password """
        return generate_password_hash(raw_password)

    def check_password(self, user_obj, raw_password):
        return check_password_hash(user_obj.password, raw_password)

    def get_by_username(self, username):
        """ Search user by its username """
        q = self.session.query(self.model).filter(
            self.model.username == username)
        user = None

        try:
            user = q.one()
        except NoResultFound:
            pass

        return user

    def get_by_email(self, email):
        q = self.session.query(self.model).filter(
            self.model.email == email)
        user = None

        try:
            user = q.one()
        except NoResultFound:
            pass

        return user
