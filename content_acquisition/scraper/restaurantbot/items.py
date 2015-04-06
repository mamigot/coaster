from scrapy.item import Item, Field


class RestaurantItem(Item):
    '''
    Information that *every* listing service should contain about a restaurant
    '''
    name = Field()
    cuisine = Field()
    description = Field()
    pricing = Field()

    street_address = Field()
    addressLocality = Field()
    addressRegion = Field()
    postalCode = Field()


class ReviewItem(Item):
    '''
    Information that *every* review should contain
    '''
    title = Field()
    text = Field()


class NYMagRestaurantItem(RestaurantItem):
    '''
    Information provided by NYMag's listing
    '''
    nymag_href = Field()
    official_href = Field()

    neighborhood = Field()
    latitude = Field()
    longitude = Field()

    avg_reader_rating = Field()
    number_reader_reviews = Field()


class NYMagReviewItem(ReviewItem):
    '''
    Information provided by NYMag's reviews
    '''
    would_go_back = Field()
    overall_rating = Field()
    food_rating = Field()
    service_rating = Field()
    decor_rating = Field()

    review_helpfulness_rating = Field()
    number_helpfulness_evaluations = Field()
