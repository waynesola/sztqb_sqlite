#!/usr/bin/python
# coding:utf-8

# 此句非必要，在多个items时可能需要用到
from items import SztqbSqliteItem
import sqlite3


class SztqbSqlitePipeline(object):
    def process_item(self, item, spider):
        if item.__class__ == SztqbSqliteItem:  # 此句非必要，在多个items时可能需要用到
            conn = sqlite3.connect('C:/Program Files/DB Browser for SQLite/database/test.db')
            cur = conn.cursor()
            # SQLite的placeholder是问号[?]，非[%s]。
            # 表名是table201701，表名不能为纯数字！
            sql = "insert into mytable(title,publish,link,text) values (?,?,?,?)"
            # 此处最后的逗号[,]不能少
            cur.execute(sql, (item['title'], item['publish'], item['link'], item['text'],))
            conn.commit()
            cur.close()
            conn.close()

        return item
