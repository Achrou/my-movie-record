# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class MomikDoubanPipeline(object):
    def process_item(self, item, spider):
        return item

class RecordSpiderPipeline(object):
    def __init__(self,mongo_host,mongo_port,mongo_db,mongo_coll,mongo_user,mongo_psw):
        # 链接数据库
        client = pymongo.MongoClient(host=mongo_host, port=mongo_port, username=mongo_user, password=mongo_psw)
        self.db = client[mongo_db]  # 获得数据库的句柄
        self.coll = self.db[mongo_coll]  # 获得collection的句柄

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_coll=crawler.settings.get('MONGO_COLL'),
            mongo_user=crawler.settings.get('MONGO_USER'),
            mongo_psw=crawler.settings.get('MONGO_PSW'),
        )
    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        self.coll.update_one({'title':postItem['title']},{'$set':postItem},upsert=True)  # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据，可以选择不写