#!/usr/bin/python
# coding:utf-8

import scrapy


class SztqbSqliteItem(scrapy.Item):
    title = scrapy.Field()
    publish = scrapy.Field()
    text = scrapy.Field()
    link = scrapy.Field()
    pass
