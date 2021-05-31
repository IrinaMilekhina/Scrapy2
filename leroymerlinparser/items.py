# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def format_price(value):
    price = int(value.replace(' ', ''))
    return price


class LeroymerlinparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose())
    params = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(format_price), output_processor=TakeFirst())
