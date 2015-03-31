# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from utils.sql import Restaurant, get_session


class StoreRestaurantItem(object):

    def process_item(self, item, spider):
        session = get_session()

        r = Restaurant( name=item['name'],
                        cuisine=item['cuisine'],
                        location=item['location'],
                        menu_href=item['menu_href'])

        # write restaurants to the database as they come
        try:
            session.add(r)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
