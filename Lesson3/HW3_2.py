from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['vacancies']
hh = db.hh
sj = db.sj


def great_salary(salary):
    i, j = True, True

    vacancy_list_hh = hh.find({'$or': [{'salary_min': {'$gte': salary}, 'salary_max': {'$gte': salary}}]},
                              {'title': 1, 'employer': 1, 'salary_min': 1, 'salary_max': 1, 'salary_currency': 1,
                               'link': 1, '_id': 0}).sort('salary_min')
    vacancy_list_sj = sj.find({'$or': [{'salary_min': {'$gte': salary}, 'salary_max': {'$gte': salary}}]},
                              {'title': 1, 'employer': 1, 'salary_min': 1, 'salary_max': 1, 'salary_currency': 1,
                               'link': 1, '_id': 0}).sort('salary_min')

    print('\nПодходящие вакансии на hh.ru:')
    for vacancy in vacancy_list_hh:
        pprint(vacancy)
        i = False
    if i:
        print('Таких вакансий на hh.ru, к сожалению, нет')

    print('\nПодходящие вакансии на superjob.ru:')
    for vacancy in vacancy_list_sj:
        pprint(vacancy)
        j = False
    if j:
        print('Таких вакансий на superjob.ru, к сожалению, нет')


salary = int(input('Введите минимальную зарплату для поиска подходящих вакансий: '))
great_salary(salary)
