# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item


class ImagePipeline(ImagesPipeline):
    # item是爬取生成的Item对象
    # 把URL字段取出 生成Request对象 加入到调度队列，等待下载
    def get_media_requests(self, item, info):
        yield Request(item['url'])

    # 这个方法用来返回保存的文件名
    # request 是当前下载对应的reuqest对象
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        print(file_name)
        return file_name

    # 当单个Item完成下载时的处理办法
    # 把下载失败的图片 过滤掉
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item
