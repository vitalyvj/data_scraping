from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    vacancy = input('Введите запрос для поиска вакансий: ')
    # pages = int(input('Введите число страниц с вакансиями (для показа всех страниц введите 0): '))
    # if pages == 0:
    #     pages = 10000
    pages = 10000

    process.crawl(HhruSpider, vacancy=vacancy, pages=pages)
    process.crawl(SjruSpider, vacancy=vacancy, pages=pages)

    process.start()
