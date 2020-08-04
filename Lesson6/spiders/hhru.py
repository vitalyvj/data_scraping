import re
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    # i = 0

    def __init__(self, vacancy, pages):
        super().__init__()
        self.start_urls = [f'https://hh.ru/search/vacancy?text={vacancy}&area=113']
        self.pages = pages

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        vacancy_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()

        for link in vacancy_links:
            yield response.follow(link, callback=self.parse_vacancies)

        if next_page: # and i < pages:
            yield response.follow(next_page, callback=self.parse)
            # i += 1

    def parse_vacancies(self, response: HtmlResponse):
        title = response.xpath("//h1/text()").extract_first()
        # salary = response.xpath("//script[@data-name='HH/GoogleDfpService']/@data-params").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        link = response.url.split('?')[0]
        employer = response.xpath("//a[@data-qa='vacancy-company-name']//span/text()").extract_first()
        _id = int(''.join(re.findall('\d', link)))

        yield JobparserItem(title=title, salary=salary, link=link, employer=employer, _id=_id)
