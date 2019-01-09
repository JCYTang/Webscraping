# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose

def get_ad_type(self, values):
    # output processor to classify the ad type
    # values is an iterator that contains the 2 xpath string that were scraped and stored for the ad_type field

    type = ''
    if 'standard-premiumplus' in values[0]:
        type = 'platinum'
    elif 'standard-elitepp' in values[0]:
        type = 'gold'
    elif 'standard-pp' in values[0]:
        type = 'silver'
    elif 'standard-standard' in values[0]:
        if len(values) > 1:
            type = 'branded'
        else:
            type = 'basic'

    return type

class DHGProperty(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass

    date = scrapy.Field()
    url = scrapy.Field()
    ad_type = scrapy.Field()
    address_line_1 = scrapy.Field()
    suburb = scrapy.Field()
    state = scrapy.Field()
    postcode = scrapy.Field()

class DHGPropertyLoader(ItemLoader):
    # set output processors
    # takefirst takes the first item in the list

    date_out = TakeFirst()

    url_in = MapCompose(str.strip)
    url_out = TakeFirst()

    ad_type_out = get_ad_type

    address_line_1_in = MapCompose(str.strip, str.title)
    address_line_1_out = TakeFirst()

    suburb_in = MapCompose(str.strip, str.upper)
    suburb_out = TakeFirst()

    state_in = MapCompose(str.strip, str.upper)
    state_out = TakeFirst()

    postcode_in = MapCompose(str.strip)
    postcode_out = TakeFirst()


