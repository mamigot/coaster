# -*- coding: utf-8 -*-

# Scrapy settings for resturantbot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'edx_bot'

SPIDER_MODULES = ['edx_bot.spiders']
NEWSPIDER_MODULE = 'edx_bot.spiders'

# http://doc.scrapy.org/en/latest/topics/item-pipeline.html#activating-an-item-pipeline-component
ITEM_PIPELINES = {
    'edx_bot.pipelines.CourseExistence': 100
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'resturantbot (+http://www.yourdomain.com)'
