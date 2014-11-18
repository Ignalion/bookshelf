"""
This module contains classe for all DB operaions in the app.
They are as below:
    BaseAbstraction
    UserAbstraction
    BookAbstraction
    AuthorAbstraction

The BaseAbstraction class contains all the low-level operations with ORM.
Other classes provide interfaces for corresponding model
"""

import itertools

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exc

from app.db import db_session
from app.lib import errors
from app import models


def safe_execute(method):
    def wrapper(self, *args, **kwargs):
        if not isinstance(self, BaseAbstraction):
            raise TypeError(
                '@safe_execute should be applied inside BaseAbstraction '
                'subclasses only'
            )
        on_success = kwargs.pop('on_success', self.save)
        on_failure = kwargs.pop('on_failure', self.revert)

        try:
            if method:
                res = method(self, *args, **kwargs)
                on_success()
                return res
            on_success()
        except exc.IntegrityError, err:
            on_failure()
            message = err.message

            raise errors.DBRecordExists(message)

    return wrapper


class BaseAbstraction(object):
    """
    Base class for other abstractions. All low-level operations like
    creating, updating or deleting objects to/from DB should be defined here
    """

    model = None

    def __init__(self, session=None):
        self.created_session = False

        if session:
            self.session = session
        else:
            self.session = self._create_session()
            self.created_session = True

    @safe_execute
    def create(self, *args, **kwargs):
        new_entry = self.model()

        for key in kwargs.iterkeys():
            setattr(new_entry, key, kwargs[key])

        self.session.add(new_entry)

    @safe_execute
    def delete(self, *args, **kwargs):
        entry_obj = self.model().query.get(kwargs.get('id'))
        if entry_obj:
            self.session.delete(entry_obj)

    @safe_execute
    def update(self, entry_obj, **kwargs):
        for key in kwargs.iterkeys():
            if hasattr(entry_obj, key):
                setattr(entry_obj, key, kwargs[key])

        self.session.add(entry_obj)

    def _create_session(self):
        return db_session

    def save(self):
        self.session.commit()

    def revert(self):
        self.session.rollback()


class UserAbstraction(BaseAbstraction):
    """ Abstraction for User model """

    model = models.User

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


class BookAbstraction(BaseAbstraction):
    """ Abstraction for Book model """

    model = models.Book

    def get_book_list(self, user_obj):
        books = user_obj.books
        return books

    def add_edit_book(self, user_obj, book):
        """ Add new book or edit existing one"""
        author_mgr = AuthorAbstraction()
        book['authors'] = author_mgr.get_author_list(user_obj).filter(
            author_mgr.model.id.in_([int(id) for id in book['authors']])).all()
        if book['id'] is not None:
            book_obj = self.model().query.get(book['id'])
            self.update(entry_obj=book_obj, **book)
        else:
            self.create(user=user_obj, **book)

    def book_search(self, title):
        books = self.session.query(self.model).filter(
            self.model.title.like('%%%s%%' % title)).all()
        return books


class AuthorAbstraction(BaseAbstraction):
    """ Abstraction for Author model """

    model = models.Author

    def get_author_list(self, user_obj):
        authors = user_obj.authors
        return authors

    def add_edit_author(self, user_obj, author):
        """ Add new author or edit existing one """
        # book_mgr = BookAbstraction()
        # author['books'] = book_mgr.get_book_list(user_obj).filter(
        #     book_mgr.model.id.in_([int(id) for id in author['books']])).all()
        if author['id'] is not None:
            author_obj = self.model().query.get(author['id'])
            self.update(entry_obj=author_obj, **author)
        else:
            self.create(user=user_obj, **author)

    def author_search(self, name):
        authors = self.session.query(self.model).filter(
            self.model.name.like('%%%s%%' % name)).all()
        books = [author.books for author in authors]
        return list(itertools.chain(*books))
