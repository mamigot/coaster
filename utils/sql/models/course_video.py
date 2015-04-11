from sqlalchemy import Column, ForeignKey, Integer, String

from utils.sql import Base


class CourseVideo(Base):
    __tablename__ = 'course_videos'

    id = Column(Integer, primary_key=True)
    subsection_id = Column(Integer, ForeignKey('course_units.id'))
    name = Column(String, nullable=False)

    transcript = Column(String)
    href = Column(String, nullable=False)

    youtube_id = Column(String(50))
    yt_views = Column(Integer)
    yt_likes = Column(Integer)
    yt_dislikes = Column(Integer)
    yt_favorites = Column(Integer)
    yt_comments = Column(Integer)
