# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from datetime import datetime
import pymysql


class InfoPipeline(object):
    def process_item(self, item, spider):
        item['crawled'] = datetime.utcnow()
        item['spider'] = spider.name
        return item

class MySQLPipeline(object):
    def __init__(self):
        # 建立链接
        self.conn = pymysql.connect('192.168.43.249', 'develop', 'poo001', 'crawl', charset='utf8')
        # 创建游标
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        # sql 语句
        insert_sql = """
        insert into chengyu(title, pronounce, paraphrase, reference, influence, link) VALUES (%s, %s, %s, %s, %s, %s);
        """
        # 执行插入数据库操作
        self.cursor.execute(insert_sql, (item['title'], item['pronounce'], item['paraphrase'],
                                         item['reference'], item['influence'], item['link']))
        # 提交
        self.conn.commit()
        return item
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


class ChengyuRedisSlaverPipeline:
    def __init__(self):
        self.file = open('chengyu.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()
