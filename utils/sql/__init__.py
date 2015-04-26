from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from config import DB_ACCESS


# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#declare-a-mapping
Base = declarative_base()


def db_connect():
    return create_engine(URL(**DB_ACCESS), echo=True)


def get_session():
    engine = db_connect()
    session = sessionmaker(bind=engine)
    return session()
