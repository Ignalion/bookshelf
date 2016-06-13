import itertools
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from base import DBObject
from _db import db_session
from app import models

DBObject.session = db_session

class UserAbstraction(DBObject):
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


class BookAbstraction(DBObject):
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


class AuthorAbstraction(DBObject):
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
