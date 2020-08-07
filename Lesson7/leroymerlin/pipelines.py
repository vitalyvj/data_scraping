# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class LeroymerlinPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.db[spider.name]

        item['primary_price'] = item['primary_price_int'] + item['primary_price_fract'] / 100
        item['second_price'] = item['second_price_int'] + item['second_price_fract'] / 100
        item['parameters'] = {key: value for key, value in zip(item['parameters_keys'], item['parameters_values'])}

        items_to_del = ['primary_price_int', 'primary_price_fract', 'second_price_int', 'second_price_fract',
                        'parameters_keys', 'parameters_values']
        [item.pop(i, None) for i in items_to_del]

        collection.update({'_id': item['_id']}, item, upsert=True)

        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            n = 1
            for img in item['photos']:
                try:
                    yield scrapy.Request(img, meta={'name': item['name'], 'file': 'file_{}'.format(str(n))})
                    n += 1
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None):
        return f"{request.meta['name']}/{request.meta['file']}.jpg"
