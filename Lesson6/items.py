# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    salary = scrapy.Field()
    employer = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary_currency = scrapy.Field()

