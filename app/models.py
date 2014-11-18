"""
This module represents all models in bookshelf applications.
There are as follows:
    User
    Book
    Author

Book and Author has Many-To-Many relationship with backref
User and Book has One-To-Many relationship with backref
User and Author has One-To-Mane relationship with backref
"""

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.db import Base


class User(Base):
    """ Represents `user` table in db """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(100))
    email = Column(String(120), index=True, unique=True)

    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username


books_authors = Table(
    'books_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)


class Book(Base):
    """ Represents `book` table in db """

    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('books', lazy='dynamic'))
    authors = relationship('Author',
                           secondary=books_authors,
                           backref='books')

    def __init__(self, title=None):
        self.title = title

    def __repr__(self):
        return '<Book %r>' % self.title


class Author(Base):
    """ Represents `author` table in db """

    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('authors', lazy='dynamic'))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Author %r>' % self.name
