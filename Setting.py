# -*- coding: utf-8 -*-

import MySQLdb
from scrapy.utils.project import get_project_settings

#Setting类 配置scrapy爬虫settings对象的参数
#包括ip池、浏览器请求头、下载设置、数据管道等
class Setting:
    # settings = get_project_settings()
    # def __int__(self):

        #创建settings对象
        settings = get_project_settings()

        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='openioc'
        )

        cur = conn.cursor()
        sqli = "select IP,PORT from proxy;"
        cursor = cur.execute(sqli)
        proxy_list = cur.fetchmany(cursor)

        # 创建settings对象
        settings = get_project_settings()

        # 设置ip池，从Mysql数据库中获取可用代理ip
        PROXIES = []
        for row in proxy_list:
            ip_port = {'ip_port': row[0] + ':' + row[1], 'user_pass': ''}
            PROXIES.append(ip_port)
        cur.close()
        conn.commit()
        conn.close()
        # #设置ip池，后期需要改为从Mysql数据库中获取可用代理ip
        # PROXIES = [
        #     {'ip_port': '110.82.46.218:8118', 'user_pass': ''},
        #     {'ip_port': '175.155.25.91:808', 'user_pass': ''},
        #     {'ip_port': '140.250.78.132:808', 'user_pass': ''},
        #     {'ip_port': '175.155.24.18:808', 'user_pass': ''},
        #     {'ip_port': '106.120.78.129:80', 'user_pass': ''},
        #     {'ip_port': '180.112.5.27:8118', 'user_pass': ''},
        #     {'ip_port': '218.86.128.127:8118', 'user_pass': ''},
        #     {'ip_port': '116.226.90.12:808', 'user_pass': ''},
        #
        # ]

        settings.set("PROXIES", PROXIES)
        #配置数据管道
        #DuplicatesPipeline：使用redis去重
        #CountDropPipline：统计丢弃item个数
        #DataBasePipeline ：把对象存入到Mysql中
        #后边的数字表示优先级，数字越小优先级越高
        settings.set("ITEM_PIPELINES", {
            'pipelines.DuplicatesPipeline': 300,
            # 'pipelines.CountDropPipline': 100,
            'pipelines.RandomUserAgent': 100,
            'pipelines.DataBasePipeline': 200,
            'pipelines.ProxyMiddleware': 110,
        })
        #配置下载中间件
        #RandomUserAgent：随机选择浏览器请求头
        #scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware：scrapy默认配置
        #ProxyMiddleware：随机选择可用的IP
        # 后边的数字表示优先级，数字越小优先级越高
        # settings.set("DOWNLOADER_MIDDLEWARES", {
        #     'pipelines.RandomUserAgent': 100,
        #     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        #     'pipelines.ProxyMiddleware': 110,
        # })
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
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        ]

        settings.set("USER_AGENTS", USER_AGENTS)

    # def getSettings(self):
    # return self.settingsSetting

#以下代码为测试代码
# # s=Setting()
# import random
# print Setting().settings.get("DOWNLOADER_MIDDLEWARES")
# print Setting().settings.get("USER_AGENTS")
