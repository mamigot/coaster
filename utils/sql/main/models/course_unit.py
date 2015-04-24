from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from utils.sql.main import Base
from course_video import CourseVideo


atable_video_unit = Table('atable_video_unit', Base.metadata,
    Column('unit_id', Integer, ForeignKey('course_units.id')),
    Column('video_id', Integer, ForeignKey('course_videos.id'))
)


class CourseUnit(Base):
    __tablename__ = 'course_units'

    id = Column(Integer, primary_key=True)
    subsection_id = Column(Integer, ForeignKey('course_subsections.id'))
    name = Column(String, nullable=False)
    href = Column(String)

    description = Column(String)

    videos = relationship('CourseVideo', secondary=atable_video_unit)
