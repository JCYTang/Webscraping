# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime, timedelta

end_of_prev_mth = datetime.today().replace(day=1) - timedelta(days=1)


class CoalItem(scrapy.Item):
    # define the fields for your item here like:
    port = scrapy.Field()
    date = scrapy.Field()
    coal = scrapy.Field()
    state = scrapy.Field()


class CoalItemLoader(ItemLoader):
    # set output processors
    # takefirst takes the first item in the list

    port_out = TakeFirst()

    date_out = TakeFirst()

    coal_out = TakeFirst()

    state_out = TakeFirst()