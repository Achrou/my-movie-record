# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
from momik_douban.GistClient import GistClient


class MomikDoubanPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonPipeline(object):
    def __init__(self, gist_key, gist_id):
        print('GIST_KEY:', gist_key, 'GIST_ID:', gist_id)
        self.gclient = GistClient(gist_key)
        self.gist_id = gist_id
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        gist_key = crawler.settings.get('GIST_KEY')
        gist_id = crawler.settings.get('GIST_ID')
        return cls(
            gist_key=os.getenv('GIST_KEY') if len(gist_key) == 0 else gist_key,
            gist_id=os.getenv('GIST_ID') if len(gist_id) == 0 else gist_id
        )

        def process_item(self, item, spider):
            key = dict(item)['type']
            print('当前类型：', key)
            if not self.files.__contains__(key):
                self.files[key] = {'line': 1, 'page': 1, 'items': []}
            file = self.files[key]
            file['items'].append(dict(item))
            if file['line'] % 15 == 0:
                file_name = 'item_' + key + '_' + str(file['page']) + '.json'
                result = self.gclient.update(self.gist_id,
                                             {"files": {file_name: {
                                                 "content": json.dumps(file['items'], ensure_ascii=False)}}})
                print('更新结果 --->', result)
                file['page'] += 1
                file['items'] = []
            file['line'] += 1
            print('当前file对象 --->', file)

            return item
