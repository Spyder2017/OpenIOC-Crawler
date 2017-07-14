# -*- coding=utf-8 -*-
__author__ = 'alphaX'

# 从西刺代理网站爬取代理IP并存入MySQL中

import urllib2, datetime
from lxml import etree
import time
import MySQLdb

class getProxy():

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.header = {"User-Agent": self.user_agent}
        # self.dbname="proxy.db"
        self.now = time.strftime("%Y-%m-%d")

    # 获取高匿IP
    def getContent(self, num):
        nn_url = "http://www.xicidaili.com/nn/" + str(num)
        #国内高匿
        req = urllib2.Request(nn_url, headers=self.header)

        global Max_Num
        global resp
        Max_Num = 6
        for i in range(Max_Num):
            try:
                resp = urllib2.urlopen(req, timeout=10)
                break
            except:
                if i < Max_Num - 1:
                    continue
                else:
                    print 'URLError: <urlopen error timed out> All times is failed '

        # resp = urllib2.urlopen(req, timeout=1000)
        content = resp.read()
        et = etree.HTML(content)
        result_even = et.xpath('//tr[@class=""]')
        result_odd = et.xpath('//tr[@class="odd"]')
        #因为网页源码中class 分开了奇偶两个class，所以使用lxml最方便的方式就是分开获取。
        #刚开始我使用一个方式获取，因而出现很多不对称的情况，估计是网站会经常修改源码，怕被其他爬虫的抓到
        #使用上面的方法可以不管网页怎么改，都可以抓到ip 和port
        for i in result_even:
            t1 = i.xpath("./td/text()")[:2]
            print "ip:%s\tport:%s" % (t1[0], t1[1])
            if self.check_dup(t1[0], t1[1]):
                if self.isAlive(t1[0], t1[1]):
                    self.insert_db(self.now,t1[0],t1[1])
        for i in result_odd:
            t2 = i.xpath("./td/text()")[:2]
            print "ip:%s\tport:%s" % (t2[0], t2[1])
            if self.check_dup(t2[0],t2[1]):
                if self.isAlive(t2[0], t2[1]):
                    self.insert_db(self.now,t2[0],t2[1])


    # 查重
    def check_dup(self,ip,port):
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='openioc'
        )
        cur = conn.cursor()
        sqli = '''select * from proxy where IP = '%s' && PORT = '%s' ''' % (str(ip), str(port))
        # print sqli
        proxy_num = cur.execute(sqli)
        row = cur.fetchmany(proxy_num)
        print proxy_num
        try:
            if proxy_num == long(0):
                return True
            else:
                print "duplicate ip '%s', not write to mysql"%row[0][1]
                return False
        except :
            print "duplicate ip '%s', not write to mysql" %row[0][1]
            return False
        cur.close()
        conn.commit()
        conn.close()


    # 插入数据库
    def insert_db(self,date,ip,port):
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='openioc'
        )
        cur = conn.cursor()
        sqli = '''
        insert into proxy (DATE,IP,PORT) VALUES ('%s','%s','%s');
        ''' % (date, ip, port)
        cur.execute(sqli)
        cur.close()
        conn.commit()
        conn.close()


    def loop(self,page):
        for i in range(1,page):
            self.getContent(i)


    #查看爬到的代理IP是否还能用
    def isAlive(self,ip,port):
        proxy = {'http':ip+':'+port}
        print proxy

        #使用这个方式是全局方法。
        proxy_support=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        #使用代理访问腾讯官网，进行验证代理是否有效
        # test_url="http://www.qq.com"
        test_url = "https://krebsonsecurity.com"
        req=urllib2.Request(test_url,headers=self.header)
        try:
            #timeout 设置为10，如果你不能忍受你的代理延时超过10，就修改timeout的数字
            resp=urllib2.urlopen(req,timeout=10)

            if resp.code==200:
                print "work"
                return True
            else:
                print "not work"
                return False
        except :
            print "Not work"
            return False


    #查看数据库里面的数据时候还有效，没有的话将其纪录删除
    def check_db_pool(self):
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='openioc'
        )
        cur = conn.cursor()
        sqli='''
        select IP,PORT from proxy;
        '''
        cursor = cur.execute(sqli)
        proxy_list = cur.fetchmany(cursor)
        for row in proxy_list:
            print row
            if not self.isAlive(row[0],row[1]):
                #代理失效， 要从数据库从删除
                delete_cmd = '''
                delete from proxy where IP='%s'
                ''' % row[0]
                print "delete IP %s in db" % row[0]
                cur.execute(delete_cmd)
                conn.commit()
        print "--------Check Out !!!-----------"
        conn.close()


if __name__ == "__main__":
    now = datetime.datetime.now()
    print "Start at %s" % now
    obj=getProxy()
    obj.check_db_pool()
    obj.loop(5)