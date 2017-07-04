# -*- coding: utf-8 -*-
from model.config import Redis
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.selector import Selector
#配置article对象，对应mysql数据库spider中的articles表
class Article(scrapy.Item):
    #字段
    title = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    publish_time = scrapy.Field()
    source_site = scrapy.Field()
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


    def parse(self, response):
        # print response.url
        sel = Selector(response)
        #获取当前页面所有的超链接
        link_in_a_page = sel.xpath('//a[@href]')
        #for循环遍历
        for link_sel in link_in_a_page:
            link = str(link_sel.re('href="(.*?)"')[0])#正则表达式提取url
            if not link.startswith('http'):#如果不是http开头，那么需要进行url拼接
                link = response.url + link
            #如果在redis数据库中存在，表明已经访问过 则无需进行重复请求 用于增量爬取
            if Redis.exists('url:%s' % link) :
                # raise DropItem("Duplicate item found: %s" % link)
                print ("Duplicate item found: %s" % link)
            elif link.startswith(self.allow_url):#过滤规则，如果url链接满足allow_url（以allow_url开头），则进行请求
                Redis.set('url:%s' % link, 1)#在redis数据库中设置为1  表示已经访问过

                yield Request(link,callback=self.parse) #递归调用，进行爬取
                article = Article() #创建article对象

                article["url"] = link   #获取网页url链接
                print sel.xpath('/html').extract()
                article["html"] = sel.xpath('/html').extract()  #获取网页html代码
                yield article   #返回article对象，返回之后，scrapy会运行DataBasePipeline函数，进行数据存储
            else:#把链接在redis数据库中设置为  避免重复请求无效url
                Redis.set('url:%s' % link, 1)

