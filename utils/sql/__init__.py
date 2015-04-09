from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from utils.sql.config import DB_ACCESS


# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#declare-a-mapping
Base = declarative_base()


''' Run before inserting or selecting items from the database '''
def create_tables():
    from models import institution, instructor, subject, course

    engine = db_connect()
    # MetaData issues CREATE TABLE statements to the database
    # for all tables that don't yet exist
    Base.metadata.create_all(engine)


def db_connect():
    return create_engine(URL(**DB_ACCESS), echo=True)


def get_session():
    # http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#creating-a-session
    # Ex.
    #   institution = Institution(name="Hogwarts")
    #   course = Course(name="Botany 101", href="http://edx.org/botany-101")
    #   subject = Subject(name="Engineering")
    #   instructor = Instructor(name="Ben Bitdiddle")
    #
    #   institution.courses.append(course)
    #   course.subjects.append(subject)
    #   course.instructors.append(instructor)
    #
    #   session = get_session()
    #   session.add(institution)
    #   session.commit()

    engine = db_connect()
    session = sessionmaker(bind=engine)
    return session()
