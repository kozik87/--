# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import hashlib
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from pymongo import MongoClient

class LeroymerlinPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                big_img = img.replace('w_82,h_82', 'w_2000,h_2000')
                try:
                    yield scrapy.Request(big_img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{item['name']}/{image_guid}.jpg"

