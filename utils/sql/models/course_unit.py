from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from utils.sql import Base


class Unit(Base):
    __tablename__ = 'course_units'

    id = Column(Integer, primary_key=True)
    subsection_id = Column(Integer, ForeignKey('course_subsections.id'))
    name = Column(String, nullable=False)

    description = Column(String)

    videos = relationship('CourseVideo', backref='course_units')
