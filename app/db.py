"""
This module represents connection to DB and contains the only
SQLAlchemy session named db_session

There is function init_db for creating all neccessary tables here.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI,
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
