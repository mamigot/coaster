from sqlalchemy import Column, ForeignKey, Integer, String
from utils.sql import Base


class NYMagListing(Base):
    '''
    Ex. http://nymag.com/listings/restaurant/apizz/
    '''
    __tablename__ = 'listings_nymag'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('_restaurants.id'))

    href = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # 1 - 4 (4 is "very expensive")
    price_range = Column(Integer)

    # 1 - 10 (10 is the highest)
    avg_reader_rating = Column(Integer)
    number_reader_reviews = Column(Integer)
