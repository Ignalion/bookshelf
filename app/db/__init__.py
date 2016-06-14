"""
This module represents connection to DB and contains the only
SQLAlchemy session named db_session

There is function init_db for creating all neccessary tables here.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI,
#                        convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
#
# Base = declarative_base()
# Base.query = db_session.query_property()
#
#
# def init_db():
#     Base.metadata.create_all(bind=engine)

engine = None
db_session = None
Base = None


def make_engine(db_uri):
    return create_engine(db_uri, convert_unicode=True)


def make_db_session(engine):
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db(db_uri):
    global engine
    global db_session
    global Base
    engine = make_engine(db_uri)
    db_session = make_db_session(engine)
    Base = declarative_base()
    Base.query = db_session.query_property()