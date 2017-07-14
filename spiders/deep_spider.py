# -*- coding: utf-8 -*-
from model.config import Redis
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, HtmlResponse
from scrapy.exceptions import DropItem
from scrapy.selector import Selector
import re
# from model.article import Article

#配置article对象，对应mysql数据库spider中的articles表
class Article(scrapy.Item):
    #字段
    url = scrapy.Field()
    # body = scrapy.Field()
    # publish_time = scrapy.Field()
    # source_site = scrapy.Field()
    html = scrapy.Field()

class DeepSpider(CrawlSpider):
    name = "Deep"

    #初始化
    #根据传入的rule规则，进行初始化Scrapy爬虫必要的参数
    def __init__(self,rule):
        self.rule = rule
        self.name = rule.name
        #域名
        self.allowed_domains = rule.allow_domains.split(",")
        #起始网址
        self.start_urls = rule.start_urls.split(",")
        #过滤规则
        self.allow_url = rule.allow_url
        # url筛选规则
        self.url_rule = rule.url_rule


    def parse(self, response):
        # print response.url
        pattern = re.compile(self.url_rule)
        link_match = pattern.match(response.url)

        sel = Selector(response)
        #获取当前页面所有的超链接
        link_in_a_page = sel.xpath('//a[@href]')

        if Redis.exists('url:%s' % response.url):
            print ("Duplicate item found: %s" % response.url)
        elif str(link_match) !=  'None':
            print ("----------------- get Article url : %s ----------------" % response.url)
            article = Article()  # 创建article对象
            article["url"] = response.url  # 获取网页url链接
            article["html"] = sel.xpath('/html').extract() #获取网页html代码
            yield article  # 返回article对象，返回之后，scrapy会运行DataBasePipeline函数，进行数据存储
        else:
            print ("not Article url , abandon url: %s " % response.url)

        Redis.set('url:%s' % response.url, 1)  # 在redis数据库中设置为1  表示已经访问过

        #for循环遍历
        for link_sel in link_in_a_page:

            link = str(link_sel.re('href="(.*?)"')[0])#正则表达式提取url
            if not link.startswith('http'):#如果不是http开头，那么需要进行url拼接
                link = response.url + link

            if Redis.exists('url:%s' % link) : #如果在redis数据库中存在，表明已经访问过 则无需进行重复请求 用于增量爬取
                print ("Duplicate item found: %s" % link)
            elif link.startswith(self.allow_url):#过滤规则，如果url链接满足allow_url（以allow_url开头），则进行请求
                yield Request(link, callback=self.parse)  # 递归调用，进行爬取

