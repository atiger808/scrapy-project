# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import redis

class FemdomRedisMasterPipeline:
    def __init__(self):
        self.REDIS_HOST = '192.168.43.249'
        self.REDIS_PORT = 6379
        self.r = redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)

    def process_item(self, item, spider):
        self.r.lpush('femdom:start_urls', item['url'])
        return item

class FemdomRedisNovelMasterPipeline:
    def __init__(self):
        self.REDIS_HOST = '192.168.43.249'
        self.REDIS_PORT = 6379
        self.r = redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)

    def process_item(self, item, spider):
        self.r.lpush('femdom_novel:start_urls', item['url'])
        return item
