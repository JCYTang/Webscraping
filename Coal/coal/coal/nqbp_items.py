# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
# from scrapy.loader.processors import TakeFirst, MapCompose
from itemloaders.processors import TakeFirst, MapCompose
from datetime import datetime, timedelta

end_of_prev_mth = datetime.today().replace(day=1) - timedelta(days=1)
# end_of_prev_mth = datetime(2020, 1, 31)


def clean_coal_data(x):
    # remove commas and strip out any spaces
    return x.replace(',', '').strip()


def get_coal_data(coal_data):
    # find index of prev month in the list and get the next value in the list which will be the coal output
    # for the prev month
    prev_mth = end_of_prev_mth.strftime('%B')
    prev_mth_idx = coal_data.index(prev_mth)
    return coal_data[prev_mth_idx + 1]


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

    coal_in = MapCompose(clean_coal_data)
    coal_out = get_coal_data

    state_out = TakeFirst()
