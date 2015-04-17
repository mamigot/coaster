from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from utils.sql import Base


class CourseVideo(Base):
    __tablename__ = 'course_videos'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    href = Column(String, nullable=False)
    transcript = Column(String)

    youtube_id = Column(String(50))
    yt_views = Column(Integer)
    yt_likes = Column(Integer)
    yt_dislikes = Column(Integer)
    yt_favorites = Column(Integer)
    yt_comments = Column(Integer)

    stats_as_of = Column(DateTime(timezone=True))
