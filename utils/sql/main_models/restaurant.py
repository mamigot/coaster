from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from utils.sql import Base


class Restaurant(Base):
    # An __init__() method is created behind the scenes
    # http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#create-an-instance-of-the-mapped-class
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cuisine = Column(String, nullable=False)
    menu_href = Column(String)

    # pricing and global_rating are based on aggregrate from all review sites
    pricing = Column(Integer)
    global_rating = Column(Integer)

    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#one-to-one
    location = relationship("Location", uselist=False, backref="restaurant")
    schedule = relationship("ScheduleEntry", backref="restaurant")

    def __repr__(self):
        return "<Restaurant(name='%s', cuisine='%s')>" % (self.name, self.cuisine)
