from sqlalchemy import Column, ForeignKey, Integer, String
from utils.sql import Base


class ScheduleEntry(Base):
    # Modeled after http://stackoverflow.com/a/2721596/2708484
    __tablename__ = '_schedules'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('_restaurants.id'))

    # 1 - Monday, 2 - Tuesday, ..., 7 - Sunday
    day_of_week = Column(Integer, nullable=False)
    # 24-hour format, e.g. 00:50, 09:30, 21:14
    opening_time = Column(String(5), nullable=False)
    closing_time = Column(String(5), nullable=False)
