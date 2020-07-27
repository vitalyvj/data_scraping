import datetime
from pprint import pprint
import requests
from lxml import html
from pymongo import MongoClient

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
           Chrome/84.0.4147.89 Safari/537.36 OPR/69.0.3686.77'}
client = MongoClient('localhost', 27017)
db = client['news']


def news_mail_ru():
    main_link = 'https://news.mail.ru'

    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)

    # Новости из шапки
    news_links = dom.xpath("//div[@class='block']//@href")

    links, news = [], []

    for link in news_links:
        if 'https://' in link:
            links.append(link)
        else:
            links.append(main_link + link)

    for link in links:
        novelty = {}

        dom_mail_news = html.fromstring(requests.get(link, headers=headers).text)
        text = dom_mail_news.xpath("//h1[@class='hdr__inner']/text()")
        source = dom_mail_news.xpath("//span[@class='note']//span[@class='link__text']/text()")
        date = dom_mail_news.xpath("//span[@class='note']//@datetime")

        novelty['text'] = text[0]
        novelty['source'] = source[0]
        novelty['date'] = date[0][:date[0].index('T')]
        novelty['link'] = link

        news.append(novelty)

    return news


def lenta_ru():
    main_link = 'https://lenta.ru'

    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)

    # Новости из шапки
    dom_lenta = dom.xpath("//a/time")

    news = []

    for item in dom_lenta:
        novelty = {}

        text = item.xpath("../text()")
        date = item.xpath("./@title")
        link = item.xpath("../@href")

        novelty['text'] = text[0].replace('\xa0', ' ')
        novelty['source'] = 'lenta.ru'
        novelty['date'] = date[0]

        if 'https://' in link[0]:
            novelty['link'] = link[0][:link[0].index('?')]
        else:
            novelty['link'] = main_link + link[0]

        news.append(novelty)

    return news


def yandex_news():
    main_link = 'https://yandex.ru'

    response = requests.get(main_link + '/news/', headers=headers)
    dom = html.fromstring(response.text)

    # Новости из основного блока
    dom_yandex = dom.xpath("//td[@class = 'stories-set__item']")
    news = []

    for item in dom_yandex:
        novelty = {}

        text = item.xpath(".//h2[@class='story__title']/a/text()")
        date = item.xpath(".//div[@class='story__date']/text()")
        link = item.xpath(".//h2[@class='story__title']/a/@href")

        novelty['text'] = text[0]
        novelty['link'] = main_link + link[0].split('?')[0]

        if 'вчера\xa0в' in date[0]:
            date = date[0].replace(' вчера\xa0в', '')
            novelty['date'] = str(datetime.date.today() - datetime.timedelta(days=1))
            novelty['source'] = date[:-6]
        else:
            novelty['date'] = str(datetime.date.today())
            novelty['source'] = date[0][:-6]

        news.append(novelty)

    return news


def fill_db(source, news):
    if source == 'mail':
        db.mail.insert_many(news)
    elif source == 'lenta':
        db.lenta.insert_many(news)
    elif source == 'yandex':
        db.yandex.insert_many(news)


fill_db('mail', news_mail_ru())
fill_db('lenta', lenta_ru())
fill_db('yandex', yandex_news())

print('\nНовости mail.ru:')
for novelty in db.mail.find({}, {'_id': 0}):
    pprint(novelty)

print('\nНовости lenta.ru:')
for novelty in db.lenta.find({}, {'_id': 0}):
    pprint(novelty)

print('\nНовости yandex.ru:')
for novelty in db.yandex.find({}, {'_id': 0}):
    pprint(novelty)
