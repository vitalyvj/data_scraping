# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import re
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['vacancies_scrapy']

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        item['salary_min'], item['salary_max'], item['salary_currency'] = self.process_salary(item['salary'])
        collection.insert_one(item)
        return item

    @staticmethod
    def process_salary(salary):
        if 'указана' in salary[0]:
            salary_min, salary_max, salary_currency = None, None, None
        elif 'договор' in salary[0]:
            salary_min, salary_max, salary_currency = None, None, None
        elif 'от' in salary[0] and 'до' in salary[2]:
            salary_min = int(''.join(re.findall('\d', salary[1])))
            salary_max = int(''.join(re.findall('\d', salary[3])))
            salary_currency = salary[-2]
        elif 'от' in salary[0] and 'месяц' in salary[4]:
            salary_min = int(''.join(re.findall('\d', salary[2])))
            salary_max = None
            salary_currency = ''.join(re.findall('\D*', salary[2]))
        elif 'от' in salary[0]:
            salary_min = int(''.join(re.findall('\d', salary[1])))
            salary_max = None
            salary_currency = salary[-2]
        elif 'до' in salary[0] and 'месяц' in salary[4]:
            salary_min = None
            salary_max = int(''.join(re.findall('\d', salary[2])))
            salary_currency = ''.join(re.findall('\D*', salary[2]))
        elif 'до' in salary[0]:
            salary_min = None
            salary_max = int(''.join(re.findall('\d', salary[1])))
            salary_currency = salary[-2]
        elif '—' in salary[2]:
            salary_min = int(''.join(re.findall('\d', salary[0])))
            salary_max = int(''.join(re.findall('\d', salary[4])))
            salary_currency = salary[-3]
        else:
            salary_min, salary_max, salary_currency = None, None, None
        return salary_min, salary_max, salary_currency
