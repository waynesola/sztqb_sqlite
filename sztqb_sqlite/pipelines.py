#!/usr/bin/python
# coding:utf-8

# 此句非必要，在多个items时可能需要用到
from items import SztqbSqliteItem
import sqlite3


class SztqbSqlitePipeline(object):
    def process_item(self, item, spider):
        if item.__class__ == SztqbSqliteItem:  # 此句非必要，在多个items时可能需要用到

            # 测试用的数据库目录地址
            conn = sqlite3.connect('C:/Program Files/DB Browser for SQLite/database/rmrb.db')

            # SQLite的数据库链接是该数据库目录地址
            # conn = sqlite3.connect('F:/程序/GitHub/flovel/database/sztqb201701.db')
            cur = conn.cursor()

            # 测试用的表
            sql = "insert into table201703(title,publish,link,text) values (?,?,?,?)"

            # SQLite的placeholder是问号[?]，非[%s]。
            # 表名是table201701，表名不能为纯数字！
            # sql = "insert into table201701(title,publish,link,text) values (?,?,?,?)"

            # 此处最后的逗号[,]不能少
            cur.execute(sql, (item['title'], item['publish'], item['link'], item['text'],))

            conn.commit()
            cur.close()
            conn.close()

        return item
