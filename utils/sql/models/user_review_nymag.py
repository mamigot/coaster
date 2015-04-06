from sqlalchemy import Column, ForeignKey, Boolean, Integer, Float, String
from utils.sql import Base


class NYMagUserReview(Base):
    __tablename__ = 'user_reviews_nymag'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('_restaurants.id'))

    title = Column(String)
    text = Column(String)

    would_go_back = Column(Boolean)
    # Ratings range from 1 - 10
    overall_rating = Column(Integer)
    food_rating = Column(Integer)
    service_rating = Column(Integer)
    decor_rating = Column(Integer)

    # Ex. "112 out of 198 people found this review helpful"
    #   review_helpfulness_rating = 112/198
    #   number_helpfulness_evaluations = 198
    review_helpfulness_rating = Column(Float)
    number_helpfulness_evaluations = Column(Integer)
