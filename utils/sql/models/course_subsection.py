from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from utils.sql import Base
from utils.sql.models.course_unit import CourseUnit


class CourseSubsection(Base):
    __tablename__ = 'course_subsections'

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey('course_sections.id'))
    name = Column(String, nullable=False)

    units = relationship('CourseUnit', backref='course_subsections')
