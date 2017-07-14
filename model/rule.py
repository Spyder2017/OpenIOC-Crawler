# -*- coding: utf-8 -*-
from sqlalchemy import Column, String , DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

#对应Mysql数据库spider中的rules表
class Rule(Base):
    #rules表名
    __tablename__ = 'rules'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    name = Column(String)
    allow_domains = Column(String)
    start_urls = Column(String)
    allow_url = Column(String)
    url_rule = Column(String)
    enable = Column(Integer)


