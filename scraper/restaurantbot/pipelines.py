# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from utils.sql import Restaurant, get_session


class StoreRestaurantItem(object):

    def process_item(self, item, spider):
        session = get_session()

        r = Restaurant()
        r['name'] = item['name']
        r['cuisine'] = item['cuisine']
        r['location'] = item['location']
        r['menu_href'] = item['menu_href']

        session.add(r)
        # write restaurant to the database immediately
        session.commit()
