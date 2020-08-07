import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroymerlin.items import LeroymerlinItem


class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        links = response.xpath("//a[@class='plp-item__info__title']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.parse_goods)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('_id', "//span[@slot='article']/@content")
        loader.add_xpath('photos', "//source[@media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_xpath('primary_price_int', "//uc-pdp-price-view[@slot = 'primary-price']/span[@slot='price']/text()")
        loader.add_xpath('primary_price_fract', "//uc-pdp-price-view[@slot = 'primary-price']/span[@slot='fract']/text()")
        loader.add_xpath('primary_unit', "//uc-pdp-price-view[@slot = 'primary-price']/span[@slot='unit']/text()")
        loader.add_xpath('second_price_int', "//uc-pdp-price-view[@slot = 'second-price']/span[@slot='price']/text()")
        loader.add_xpath('second_price_fract', "//uc-pdp-price-view[@slot = 'second-price']/span[@slot='fract']/text()")
        loader.add_xpath('second_unit', "//uc-pdp-price-view[@slot = 'second-price']/span[@slot='unit']/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('parameters_keys', "//dt/text()")
        loader.add_xpath('parameters_values', "//dd/text()")
        yield loader.load_item()
