# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
from scrapy import signals
from momik_douban.GistClient import GistClient
from github import Github


class JsonPipeline(object):
    def __init__(self, gist_key, gist_id):
        print('GIST_KEY:', gist_key, 'GIST_ID:', gist_id)
        self.gclient = GistClient(gist_key)
        self.g = Github(gist_key)
        self.repo = self.g.get_repo("Achrou/my-movie-record")
        self.gist_id = gist_id
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        gist_key = crawler.settings.get('GIST_KEY')
        gist_id = crawler.settings.get('GIST_ID')
        pipeline = cls(
            gist_key=os.getenv('GIST_KEY') if len(gist_key) == 0 else gist_key,
            gist_id=os.getenv('GIST_ID') if len(gist_id) == 0 else gist_id
        )

        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        print('START--> 上传数据至Gist', self.files.keys())
        record_count = {}

        for key in self.files.keys():
            items = self.files[key]
            record_count[key] = len(items)
            items.sort(key=lambda t: t['date'], reverse=True)

            line = 1
            page = 1
            page_items = []
            for item in items:
                page_items.append(item)
                if line % 15 == 0:
                    file_name = 'item_' + key + '_' + str(page) + '.json'
                    # self.gclient.update(self.gist_id,
                    #                     {"files": {file_name: {
                    #                         "content": json.dumps(page_items, ensure_ascii=False)}}})
                    self.saveData(file_name, json.dumps(page_items, ensure_ascii=False))
                    page += 1
                    page_items = []
                line += 1

        print('采集结果--->:', record_count)
        # self.gclient.update(self.gist_id,
        #                     {"files": {'record_count': {
        #                         "content": json.dumps(record_count, ensure_ascii=False)}}})
        self.saveData("record_count", json.dumps(record_count, ensure_ascii=False))

    def process_item(self, item, spider):
        key = item['type']
        if not self.files.__contains__(key):
            self.files[key] = []
        self.files[key].append(dict(item))
        return item

    def saveData(self, file_name, content):
        try:
            contents = self.repo.get_contents(file_name, ref="db")
            self.repo.update_file(contents.path, "update data", content, contents.sha, branch="db")
        except:
            self.repo.create_file(file_name, "update data", content, branch="db")
