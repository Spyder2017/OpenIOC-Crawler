# -*- coding: utf-8 -*-
from sqlalchemy import Column, String , DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    #表结构
    id = Column(Integer, primary_key=True)
    url = Column(String)
    # body = Column(String)
    # is_extract = Column(Integer)
    # count = Column(Integer)
    html = Column(String)
