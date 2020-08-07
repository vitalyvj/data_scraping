# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def clear_price(value):
    value = value.replace(' ', '')
    return float(value)


def copecks(value):
    if value:
        return float(value[0])
    else:
        return float(0)


def clear_parameters(value):
    value = ' '.join(list(filter(None, value.replace('\n', '').split(' '))))
    return value


class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field(output_processor=TakeFirst())
    primary_price_int = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_price))
    primary_price_fract = scrapy.Field(input_processor=MapCompose(copecks))
    primary_unit = scrapy.Field(output_processor=TakeFirst())
    second_price_int = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_price))
    second_price_fract = scrapy.Field(input_processor=MapCompose(copecks))
    second_unit = scrapy.Field(output_processor=TakeFirst())
    primary_price = scrapy.Field()
    second_price = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    parameters_keys = scrapy.Field(input_processor=MapCompose(clear_parameters))
    parameters_values = scrapy.Field(input_processor=MapCompose(clear_parameters))
    parameters = scrapy.Field()
