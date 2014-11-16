from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(100))
    email = Column(String(120), index=True, unique=True)

    def __init__(self, username=None, email=None):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

books_authors = Table('books_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    authors = relationship('Author',
                             secondary=books_authors)

    def __init__(self, title=None):
       self.title = title

    def __repr__(self):
        return '<Book %r>' % self.title

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Author %r>' % self.name

