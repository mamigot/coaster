from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from utils.sql.config import DB_ACCESS


# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#declare-a-mapping
Base = declarative_base()


''' Run before inserting or selecting items from the database '''
def create_tables():
    from models import institution, instructor, subject, \
        course, course_section, course_subsection, course_unit, course_video

    engine = db_connect()
    # MetaData issues CREATE TABLE statements to the database
    # for all tables that don't yet exist
    Base.metadata.create_all(engine)


def db_connect():
    return create_engine(URL(**DB_ACCESS), echo=True)


def get_session():
    engine = db_connect()
    session = sessionmaker(bind=engine)
    return session()
