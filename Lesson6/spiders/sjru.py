import re
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    # i = 0

    def __init__(self, vacancy, pages):
        super().__init__()
        self.start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={vacancy}']
        self.pages = pages

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        vacancy_links = response.xpath("//a[contains(@class,'_6AfZ9')]/@href").extract()

        for link in vacancy_links:
            yield response.follow(link, callback=self.parse_vacancies)

        if next_page: # and i < pages:
            yield response.follow(next_page, callback=self.parse)
            # i += 1

    def parse_vacancies(self, response: HtmlResponse):
        title = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//span[@class='_1OuF_ ZON4b']//text()").extract()
        link = response.url.split('?')[0]
        employer = response.xpath("//a/h2/text()").extract_first()
        _id = int(''.join(re.findall('\d', link)))

        yield JobparserItem(title=title, salary=salary, link=link, employer=employer, _id=_id)
