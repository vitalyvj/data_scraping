import re
from pprint import pprint
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


def request_hh(main_link, params):
    response = requests.get(main_link, headers=headers, params=params)
    soup = bs(response.text, 'lxml')
    vac_block = soup.find('div', {'class': 'vacancy-serp'})
    next_page = soup.find('a', {'data-qa': 'pager-next'})
    return vac_block, next_page


def request_sj(main_link, params):
    response = requests.get(main_link, headers=headers, params=params)
    soup = bs(response.text, 'lxml')
    vac_block = soup.find('div', {'class': '_1ID8B'})
    next_page = soup.find('span', {'class': '_3IDf-'}, text='Дальше')
    return vac_block, next_page


def salary_parsing(salary):
    salary_currency = re.findall('\D*', salary)[-2][1:]
    if 'договор' in salary:
        salary_min, salary_max, salary_currency = None, None, None
    elif '-' in salary:
        salary_min = int(''.join(re.findall('\d', salary.split('-')[0])))
        salary_max = int(''.join(re.findall('\d', salary.split('-')[1])))
    elif '—' in salary:
        salary_min = int(''.join(re.findall('\d', salary.split('—')[0])))
        salary_max = int(''.join(re.findall('\d', salary.split('—')[1])))
    elif 'от' in salary:
        salary_min = int(''.join(re.findall('\d', salary)))
        salary_max = None
    elif 'до' in salary:
        salary_min = None
        salary_max = int(''.join(re.findall('\d', salary)))
    else:
        salary_min, salary_max, salary_currency = None, None, None
    return salary_min, salary_max, salary_currency


def hh_scraping(vac_block_hh):
    # vac_list = vac_block_hh.find_all('div', {'data-qa':'vacancy-serp__vacancy'})
    vac_list = vac_block_hh.findChildren(recursive=False)

    for vac in vac_list:
        vac_data = {}

        title = vac.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        if title:
            vac_data['title'] = title.getText()
        else:
            continue

        link = title['href']
        vac_data['link'] = link[:link.index('?')]

        employer = vac.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
        if employer:
            employer = employer.getText()
            if employer[0] == ' ':
                employer = employer[1:]
            vac_data['employer'] = employer

        salary = vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if salary:
            salary = salary.getText()
            salary_min, salary_max, salary_currency = salary_parsing(salary)
            vac_data['salary_min'] = salary_min
            vac_data['salary_max'] = salary_max
            vac_data['salary_currency'] = salary_currency
        else:
            vac_data['salary_min'], vac_data['salary_max'], vac_data['salary_currency'] = None, None, None

        vac_data['site'] = 'hh.ru'

        vacancies.append(vac_data)

    return vacancies


def sj_scraping(vac_block_sj):
    vac_list = vac_block_sj.find_all('div', {'class': '_2g1F-'})
    # vac_list = vac_block_sj.findChildren(recursive=False)

    for vac in vac_list:
        vac_data = {}

        title = vac.find('a', {'class': '_1UJAN'})
        if title:
            vac_data['title'] = title.getText()
        else:
            continue

        link = title['href']
        vac_data['link'] = 'https://russia.superjob.ru/' + link

        employer = vac.find('a', {'class': '_25-u7'})
        if employer:
            employer = employer.getText()
            vac_data['employer'] = employer

        salary = vac.find('span', {'class': '_2VHxz'})
        if salary:
            salary = salary.getText()
            salary_min, salary_max, salary_currency = salary_parsing(salary)
            vac_data['salary_min'] = salary_min
            vac_data['salary_max'] = salary_max
            vac_data['salary_currency'] = salary_currency
        else:
            vac_data['salary_min'], vac_data['salary_max'], vac_data['salary_currency'] = None, None, None

        vac_data['site'] = 'superjob.ru'

        vacancies.append(vac_data)

    return vacancies


vacancy = input('Введите запрос для поиска вакансий: ')
pages = int(input('Введите число страниц с вакансиями (для показа всех страниц введите 0): '))
if pages == 0:
    pages = 100000

# vacancy = 'data scientist'
# pages = 2

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
           Chrome/84.0.4147.89 Safari/537.36 OPR/69.0.3686.77'}
link_hh = 'https://hh.ru/search/vacancy/'
link_sj = 'https://russia.superjob.ru/vacancy/search/'
vacancies = []

i = 0
next_page_hh = True
while next_page_hh and i + 1 <= pages:
    params_hh = {'text': vacancy, 'area': 113, 'page': i}
    vac_block_hh, next_page_hh = request_hh(link_hh, params_hh)
    vacancies = hh_scraping(vac_block_hh)
    i += 1

j = 0
next_page_sj = True
while next_page_sj and j + 1 <= pages:
    params_sj = {'keywords': vacancy, 'page': j}
    vac_block_sj, next_page_sj = request_sj(link_sj, params_sj)
    vacancies = sj_scraping(vac_block_sj)
    j += 1

# pprint(vacancies)
print('Найдено вакансий:', len(vacancies))

df = pd.DataFrame(vacancies)
# pd.set_option('display.max_columns', len(df.columns))
# pd.set_option('display.max_rows', len(df))
df.index += 1
pprint(df)
