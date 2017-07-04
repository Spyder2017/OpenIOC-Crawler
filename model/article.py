# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

class Article(scrapy.Item):
    #字段
    title = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    publish_time = scrapy.Field()
    source_site = scrapy.Field()
    html = scrapy.Field()