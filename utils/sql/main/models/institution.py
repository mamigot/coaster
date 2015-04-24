from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from utils.sql.main import Base
from course import Course


class Institution(Base):
    __tablename__ = 'institutions'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    courses = relationship("Course")
