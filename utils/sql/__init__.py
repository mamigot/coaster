from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from utils.sql.config import DB_ACCESS


# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#declare-a-mapping
Base = declarative_base()


''' Run before inserting or selecting items from the database '''
def create_tables():
    from models import _restaurant, _location, _schedule_entry, \
    listing_nymag, user_review_nymag

    engine = db_connect()
    # MetaData issues CREATE TABLE statements to the database
    # for all tables that don't yet exist
    Base.metadata.create_all(engine)


def db_connect():
    return create_engine(URL(**DB_ACCESS), echo=True)


def get_session():
    # http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#creating-a-session
    # Ex.
    #   r = Restaurant(name="Grand Appetito", cuisine="Italian")
    #   lo = Location(latitude=123.111, longitude=4.0)
    #   se = ScheduleEntry(day_of_week=2, opening_time="03:12", closing_time="04:00")
    #   r.location = lo
    #   r.schedule.append(se)
    #
    #   session = get_session()
    #   session.add(r)
    #   session.commit()

    engine = db_connect()
    session = sessionmaker(bind=engine)
    return session()
