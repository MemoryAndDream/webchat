# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import settings
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class ChouqianPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = MySQLdb.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();


    def process_item(self, item, spider):
        self.insert_into_table(self.cursor,item)
        return item

    def insert_into_table(self, cursor, item):
        sql =  'insert into wechat_qian(title,page_url,img_url) values("%s","%s","%s")'%(
                MySQLdb.escape_string(item['title']), MySQLdb.escape_string(item['page_url']), MySQLdb.escape_string(item['img_url']))
        cursor.execute(sql)
        self.connect.commit()


class MysqlPipeline2(object):
    def __init__(self):
        # 连接数据库
        self.connect = MySQLdb.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();


    def process_item(self, item, spider):
        self.insert_into_table(self.cursor,item)
        return item

    def insert_into_table(self, cursor, item):
        sql =  'insert into alibaba_data(title,category,QuickDetails,category_id,url) values("%s","%s","%s","%s","%s")'%(
                MySQLdb.escape_string(item['title']),
                MySQLdb.escape_string(item['category']), MySQLdb.escape_string(item['QuickDetails']),
                MySQLdb.escape_string(item['category_id']),MySQLdb.escape_string(item['url']))
        cursor.execute(sql)
        self.connect.commit()

