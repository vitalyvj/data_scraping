import HW2_with_id as HW2
from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['vacancies']
hh = db.hh
sj = db.sj


def fill_db(vacancies):
    for vac in vacancies:
        if vac['site'] == 'hh.ru':
            hh.insert_one(vac)
        if vac['site'] == 'superjob.ru':
            sj.insert_one(vac)


vacancy = input('Введите запрос для поиска вакансий: ')
pages = int(input('Введите число страниц с вакансиями (для показа всех страниц введите 0): '))
if pages == 0:
    pages = 100000

vacancies = HW2.execute(vacancy, pages)
hh.drop()
sj.drop()
fill_db(vacancies)

print('Найдено вакансий:', len(vacancies))
print('\tиз них на hh.ru', len(list(hh.find())))
print('\tиз них на superjob.ru', len(list(sj.find())))
