from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from utils.sql import Base
from utils.sql.models.subject import Subject
from utils.sql.models.instructor import Instructor
from utils.sql.models.course_section import CourseSection


# http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#many-to-many
atable_course_subject = Table('atable_course_subject', Base.metadata,
    Column('subject_id', Integer, ForeignKey('subjects.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

atable_course_instructor = Table('atable_course_instructor', Base.metadata,
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
    # The timezone is UTC (use datetime.utcnow)
    last_crawled_on = Column(DateTime(timezone=True))

    # A course may have multiple subjects
    subjects = relationship("Subject", secondary=atable_course_subject)
    instructors = relationship("Instructor", secondary=atable_course_instructor)

    # Course data
    sections = relationship("CourseSection", backref="courses")
