# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MomikDoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DoubanRecordItem(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()
    pic = scrapy.Field()
    intro = scrapy.Field()
    date = scrapy.Field()
    rating = scrapy.Field()
    ratingNum = scrapy.Field()
    type = scrapy.Field()
    comment = scrapy.Field()
    modiTime = scrapy.Field()
