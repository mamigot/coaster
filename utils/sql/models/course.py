from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from utils.sql import Base


# http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#many-to-many
course_subject_atable = Table('course_subject_atable', Base.metadata,
    Column('subject_id', Integer, ForeignKey('subjects.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

course_instructor_atable = Table('course_instructor_atable', Base.metadata,
    Column('instructor_id', Integer, ForeignKey('instructors.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)


class Course(Base):
    '''
    See course field examples here: https://www.edx.org/search/api/all
    '''
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    edx_guid = Column(Integer)
    edx_code = Column(String(30))
    institution_id = Column(Integer, ForeignKey('institutions.id'))

    name = Column(String, nullable=False)
    href = Column(String, nullable=False)

    availability = Column(String)
    start = Column(String)
    crawled_on = Column(DateTime, default=datetime.utcnow)

    # A course may have multiple subjects
    subjects = relationship("Subject", secondary=course_subject_atable)
    instructors = relationship("Instructor", secondary=course_instructor_atable)
