# -*- coding: utf-8 -*-
import datetime
from spiders.deep_spider import DeepSpider
from model.config import DBSession
from model.rule import Rule
from scrapy.crawler import CrawlerProcess
from model.XiciProxy import getProxy

from Setting import Setting
#爬虫主函数

now = datetime.datetime.now()
print "Start at %s" % now
# 更新代理IP
obj=getProxy()
obj.check_db_pool()
obj.loop(5)

process = CrawlerProcess(Setting().settings)

db = DBSession()
#获取Mysql数据库spider中rules表中enable=1的规则信息
rules = db.query(Rule).filter(Rule.enable == 1)
#for循环遍历规则信息
for rule in rules:
    #调用DeepSpider进行递归爬取，rule为参数对应rules表中的一条记录信息
    process.crawl(DeepSpider,rule)
#启动爬虫
process.start()


