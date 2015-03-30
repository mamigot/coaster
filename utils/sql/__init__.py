from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from utils.sql.config import DB_ACCESS


# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#declare-a-mapping
Base = declarative_base()


''' Define table metadata '''
class Restaurant(Base):
    # An __init__() method is created behind the scenes
    # http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#create-an-instance-of-the-mapped-class
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cuisine = Column(String, nullable=False)
    location = Column(String(100), nullable=False)
    hours = Column(Integer)
    menu_href = Column(String)

    # pricing and global_rating are based on aggregrate from all review sites
    pricing = Column(Integer)
    global_rating = Column(Integer)

    def __repr__(self):
        return "<Restaurant(name='%s', cuisine='%s')>" % (self.name, self.cuisine)



def create_tables():
    engine = db_connect()
    # MetaData issues CREATE TABLE statements to the database
    # for all tables that don't yet exist
    Base.metadata.create_all(engine)


def db_connect():
    return create_engine(URL(**DB_ACCESS), echo=True)


def get_session():
    # http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#creating-a-session
    # Ex.
    #   session = get_session()
    #   r = Restaurant(name="Grand Appetito", cuisine="Italian")
    #   session.add(r)
    #   session.commit()

    engine = db_connect()
    session = sessionmaker(bind=engine)
    return session()
