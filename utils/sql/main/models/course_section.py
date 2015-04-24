from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from utils.sql.main import Base
from course_subsection import CourseSubsection


class CourseSection(Base):
    __tablename__ = 'course_sections'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    name = Column(String, nullable=False)

    subsections = relationship('CourseSubsection', backref='course_sections')
