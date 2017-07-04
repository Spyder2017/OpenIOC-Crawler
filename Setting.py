# -*- coding: utf-8 -*-
from scrapy.utils.project import get_project_settings

#Setting类 配置scrapy爬虫settings对象的参数
#包括ip池、浏览器请求头、下载设置、数据管道等
class Setting:
    # settings = get_project_settings()
    # def __int__(self):

        #创建settings对象
        settings = get_project_settings()

        #设置ip池，后期需要改为从Mysql数据库中获取可用代理ip
        PROXIES = [
            # {'ip_port': '110.82.46.218:8118', 'user_pass': ''},
            # {'ip_port': '175.155.25.91:808', 'user_pass': ''},
            # {'ip_port': '140.250.78.132:808', 'user_pass': ''},
            # {'ip_port': '175.155.24.18:808', 'user_pass': ''},
            # {'ip_port': '106.120.78.129:80', 'user_pass': ''},
            # {'ip_port': '180.112.5.27:8118', 'user_pass': ''},
            #
            # {'ip_port': '218.86.128.127:8118', 'user_pass': ''},
            # {'ip_port': '116.226.90.12:808', 'user_pass': ''},
            {'ip_port': '124.118.212.46:8118', 'user_pass': ''},
            {'ip_port': '115.46.84.224:8118', 'user_pass': ''},

        ]

        settings.set("PROXIES", PROXIES)
        #配置数据管道
        #DuplicatesPipeline：使用redis去重
        #CountDropPipline：统计丢弃item个数
        #DataBasePipeline ：把对象存入到Mysql中
        #后边的数字表示优先级，数字越小优先级越高
        settings.set("ITEM_PIPELINES", {
            # 'pipelines.DuplicatesPipeline': 200,
            # 'pipelines.CountDropPipline': 100,
            # 'pipelines.RandomUserAgent': 100,
            'pipelines.DataBasePipeline': 300,
        })
        #配置下载中间件
        #RandomUserAgent：随机选择浏览器请求头
        #scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware：scrapy默认配置
        #ProxyMiddleware：随机选择可用的IP
        # 后边的数字表示优先级，数字越小优先级越高
        settings.set("DOWNLOADER_MIDDLEWARES", {
            'pipelines.RandomUserAgent': 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
            'pipelines.ProxyMiddleware': 110,
        })
        import random
        # 配置一些下载相关的参数，详细说明参考说明文档
        setting_map = {"DOWNLOAD_DELAY": 5, "CONCURRENT_REQUESTS_PER_DOMAIN": 10, "CONCURRENT_REQUESTS_PER_IP": 10,
                       "COOKIES_ENABLED": False, "AUTOTHROTTLE_ENABLED": True, "AUTOTHROTTLE_START_DELAY": 2,
                       "AUTOTHROTTLE_MAX_DELAY": 60, "AUTOTHROTTLE_DEBUG": False
                       }

        for k in setting_map:
            settings.set(k, setting_map[k])
        #配置浏览器请求头列表
        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]


        settings.set("USER_AGENTS", USER_AGENTS)

    # def getSettings(self):
    #     return self.settingsSetting

#以下代码为测试代码
# s=Setting()
import random
print Setting().settings.get("DOWNLOADER_MIDDLEWARES")
print Setting().settings.get("USER_AGENTS")
