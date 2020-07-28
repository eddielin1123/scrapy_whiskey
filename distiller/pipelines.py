# -*- coding: utf-8 -*-
from pymongo import MongoClient

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exporters import JsonItemExporter
from scrapy.exporters import CsvItemExporter
from scrapy import signals

class MongoDBPipeline:
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI')
        db_name = spider.settings.get('MONGODB_DB_NAME')
        db_coll = spider.settings.get('MONGODB_DB_COL')
        self.db_client = MongoClient('mongodb://eddie:eb102@35.194.200.244:27017/')
        self.db = self.db_client[db_name][db_coll]

    def process_item(self, item, spider):
        self.insert_article(item)
        return item

    def insert_article(self, item):
        item = dict(item)
        self.db.article.insert_one(item)

    def close_spider(self, spider):
        self.db_client.close()

# class CSVPipeline(object):
#
#   def __init__(self):
#     self.files = {}
#
#   @classmethod
#   def from_crawler(cls, crawler):
#     pipeline = cls()
#     crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
#     crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
#     return pipeline
#
#   def spider_opened(self, spider):
#     file = open('%s_items.csv' % spider.name, 'w+b')
#     self.files[spider] = file
#     self.exporter = CsvItemExporter(file)
#     self.exporter.fields_to_export = []
#     self.exporter.start_exporting()
#
#   def spider_closed(self, spider):
#     self.exporter.finish_exporting()
#     file = self.files.pop(spider)
#     file.close()
#
#   def process_item(self, item, spider):
#     self.exporter.export_item(item)
#     return item

#
# class JsonExporterPipeline(object):
#     def __init__(self):
#         self.file = open('distiller_comment.json', 'wb')
#         self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
#         # 開始寫入
#         self.exporter.start_exporting()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     def open_spider(self, spider):
#         print('爬虫开始')
#         pass
#
#     def close_spider(self, spider):
#         # 完成寫入
#         self.exporter.finish_exporting()
#         self.file.close()
#         pass

class DistillerPipeline:
    def process_item(self, item, spider):
        return item
