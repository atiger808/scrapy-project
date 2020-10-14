# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import redis

class Shop168RedisMasterPipeline:
    def __init__(self):
        # 初始化连接数据的变量
        self.REDIS_HOST = '192.168.43.249'
        self.REDIS_PORT = 6379
        # 连接redis
        self.r = redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)

    def process_item(self, item, spider):
        # 向redis中插入需要爬取的链接
        self.r.lpush('shop168:start_urls', item['url'])
        return item
