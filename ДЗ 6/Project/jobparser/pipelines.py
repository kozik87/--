# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary_hh(item['salary'])
            del item['salary']
        if spider.name == 'sjru':
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary_sj(item['salary'])
            del item['salary']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        salary_min = None
        salary_max = None
        currency = None
        str = ''.join(salary[:-1]).replace(u'\xa0', '')
        pattern = re.compile(r'от (?P<salary_start2>[0-9]+) до (?P<salary_end2>[0-9]+) (?P<valute3>([\w]+))|^от (?P<salary_start1>[0-9]+) (?P<valute1>([\w]+))|^до (?P<salary_end1>[0-9]+) (?P<valute2>([\w]+))', re.IGNORECASE)
        m = pattern.match(str)
        if m:
            if m.group('salary_start1') or m.group('salary_start2'):
                salary_min = int(m.group('salary_start1') or m.group('salary_start2'))
            if m.group('salary_end1') or m.group('salary_end2'):
                salary_max = int(m.group('salary_end1') or m.group('salary_end2'))
            currency = m.group('valute1') or m.group('valute2') or m.group('valute3')
        return salary_min, salary_max, currency

    def process_salary_sj(self, salary):
        salary_min = None
        salary_max = None
        currency = None
        str = ' '.join(salary).replace(u'\xa0', '')
        pattern = re.compile(r'(?P<salary_start2>[0-9]+) (?P<salary_end2>[0-9]+)  (?P<valute3>([\w]+))|^от  (?P<salary_start1>[0-9]+)(?P<valute1>([\w]+))|^до  (?P<salary_end1>[0-9]+)(?P<valute2>([\w]+))', re.IGNORECASE)
        m = pattern.match(str)
        if m:
            if m.group('salary_start1') or m.group('salary_start2'):
                salary_min = int(m.group('salary_start1') or m.group('salary_start2'))
            if m.group('salary_end1') or m.group('salary_end2'):
                salary_max = int(m.group('salary_end1') or m.group('salary_end2'))
            currency = m.group('valute1') or m.group('valute2') or m.group('valute3')
        return salary_min, salary_max, currency

