#!/usr/bin/python
# coding:utf-8

import scrapy
from bs4 import BeautifulSoup
import arrow
import urlparse
import datetime
from ..items import SztqbSqliteItem


class AllArticles(scrapy.Spider):
    name = "test"
    allowed_domains = ["sznews.com"]
    start_urls = [
        "http://sztqb.sznews.com"
    ]

    # 爬取指定天数的报纸
    def parse(self, response):
        start = datetime.datetime(2017, 5, 1)
        end = datetime.datetime(2017, 5, 1)
        for r in arrow.Arrow.range('day', start, end):
            year_month = r.format('YYYY-MM')
            day = r.format('DD')
            url = "http://sztqb.sznews.com/html/" + year_month + "/" + day + "/node_642.htm"
            yield scrapy.Request(url, callback=self.parse_item)

    # 爬取当天所有非广告、天气或公告的文章
    def parse_item(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        ts = soup.find('div', attrs={"style": "height:730px; overflow-y:scroll; width:100%;"}) \
            .find_all('table',
                      width="100%",
                      border="0",
                      cellspacing="1",
                      cellpadding="0")
        for t in ts:
            als = t.find('table', cellspacing="0", cellpadding="1", border="0").tbody.find_all('a')
            for al in als:
                item = SztqbSqliteItem()
                if (al.div.get_text() != u"广告") & (al.div.get_text() != u"今日天气") & (al.div.get_text() != u"公告"):
                    item['title'] = al.div.get_text()
                    # 根据当前url（当天首页）和文章相对路径，补全绝对路径
                    link = urlparse.urljoin(response.url, al.get('href'))
                    item['link'] = link
                    item['publish'] = soup.find('table', id="logoTable"). \
                        find('td', width="204", align="center", valign="top").get_text()
                    request_article = scrapy.Request(link, callback=self.parse_article)
                    # 不同parse()之间传递item值需要meta['item']
                    request_article.meta['item'] = item
                    yield request_article

    # 爬取某一篇文章正文内容
    def parse_article(self, response):
        item = response.meta['item']
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        temp = "\n    "
        ps = soup.find('founder-content').find_all('p')
        for p in ps:
            temp += p.get_text()
            temp += "\n    "
        item['text'] = temp
        yield item
