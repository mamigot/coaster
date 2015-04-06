from scrapy.item import Item, Field


class RestaurantItem(Item):
    '''
    Information that *every* listing service should have about a restaurant
    '''
    name = Field()
    cuisine = Field()
    description = Field()
    pricing = Field()

    street_address = Field()
    addressLocality = Field()
    addressRegion = Field()
    postalCode = Field()


class NYMagRestaurantItem(RestaurantItem):
    '''
    Information provided by NYMag
    '''
    nymag_href = Field()
    official_href = Field()

    neighborhood = Field()
    latitude = Field()
    longitude = Field()

    avg_reader_rating = Field()
    number_reader_reviews = Field()
