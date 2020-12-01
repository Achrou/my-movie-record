# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from momik_douban.GistClient import GistClient


class JsonPipeline(object):
    def __init__(self, gist_key, gist_id):
        self.gclient = GistClient(gist_key)
        self.gist_id = gist_id
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            gist_key=crawler.settings.get('GIST_KEY'),
            gist_id=crawler.settings.get('GIST_ID')
        )

    def process_item(self, item, spider):
        key = item['type']
        if not self.files.__contains__(key):
            self.files[key] = {'line': 1, 'page': 1, 'items': []}
        file = self.files[key]
        file.items.append(dict(item))
        if file.line % 15 == 0:
            file_name = 'item_' + key + '_' + str(file.page) + '.json'
            self.gclient.update(self.gist_id,
                                {"files": {file_name: {"content": json.dumps(file.items, ensure_ascii=False)}}})
            file.items.page += 1
            file.items = []
        file.items.line += 1

        return item
