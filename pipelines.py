# -*- coding: utf-8 -*-

import json
import codecs
from scrapy.exceptions import DropItem
from model.config import DBSession
from model.config import Redis
from model.article import Article

# 去重
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if type(item) == type(None):
            raise DropItem("Duplicate item found: %s" % item)
        elif Redis.exists('url:%s' % item['url']):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            Redis.set('url:%s' % item['url'],1)
            return item

# 存储到数据库
class DataBasePipeline(object):
    def open_spider(self, spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        a = Article(url=item["url"],html=item["html"])
        # print a.title
        self.session.add(a)
        self.session.commit()

    def close_spider(self,spider):
        self.session.close()

# 存储到文件
class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('items.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode('unicode_escape'))
        return item

# 爬取指定条数 100条
class CountDropPipline(object):
    def __init__(self):
        self.count = 100

    def process_item(self, item, spider):
        if self.count == 0:
            raise DropItem("Over item found: %s" % item)
        else:
            self.count -= 1
            return item


import random
import base64
from scrapy.utils.project import get_project_settings
from Setting import Setting
#随机选择浏览器请求头
class RandomUserAgent(object):
    def __init__(self,agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(Setting.settings.get("USER_AGENTS"))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(Setting.settings.get("USER_AGENTS")))

#设置可用代理ip
class ProxyMiddleware(object):

    def process_request(self, request,spider):
        settings = Setting.settings
        proxy = random.choice(settings.get("PROXIES"))

        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            request.headers['Proxy-Authorization'] = 'Basic ' + proxy['user_pass']
            print("**************ProxyMiddleware have pass************", proxy['ip_port'])
        else:
            print("**************ProxyMiddleware no pass************", proxy['ip_port'])
            request.meta['proxy'] = "http://%s" % proxy['ip_port']