# -*- coding: utf-8 -*-

# Scrapy settings for resturantbot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'restaurantbot'

SPIDER_MODULES = ['restaurantbot.spiders']
NEWSPIDER_MODULE = 'restaurantbot.spiders'

ITEM_PIPELINES = [
    'restaurantbot.pipelines.StoreRestaurantItem'
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'resturantbot (+http://www.yourdomain.com)'
