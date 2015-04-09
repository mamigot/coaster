from sqlalchemy import Column, Integer, String
from utils.sql import Base


class Instructor(Base):
    __tablename__ = 'instructors'

    id = Column(Integer, primary_key=True)
    edx_nid = Column(Integer)
    name = Column(String, nullable=False)
