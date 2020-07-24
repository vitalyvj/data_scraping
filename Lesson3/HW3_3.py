import HW2_with_id as HW2
from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['vacancies']
hh = db.hh
sj = db.sj

vac_quantity = len(list(hh.find())) + len(list(sj.find()))


def fill_new(vacancies):
    i, j = 0, 0
    for vac in vacancies:
        if vac['site'] == 'hh.ru' and not hh.find_one({'id': vac['id']}):
            hh.insert_one(vac)
            i += 1
        if vac['site'] == 'superjob.ru' and not sj.find_one({'id': vac['id']}):
            sj.insert_one(vac)
            j += 1
    return i, j


vacancy = input('Введите запрос для поиска вакансий: ')
pages = int(input('Введите число страниц с вакансиями (для показа всех страниц введите 0): '))
if pages == 0:
    pages = 100000

vacancies = HW2.execute(vacancy, pages)
i, j = fill_new(vacancies)

print('Найдено новых вакансий:', len(list(hh.find())) + len(list(sj.find())) - vac_quantity)
print('\tиз них на hh.ru', i)
print('\tиз них на superjob.ru', j)
