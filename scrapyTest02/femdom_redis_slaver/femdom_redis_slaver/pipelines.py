# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from datetime import datetime

class InfoPipeline(object):
    def process_item(self, item, spider):
        item['crawled'] = datetime.utcnow()
        item['spider'] = spider.name
        return item

# 视频
class FemdomRedisSlaverPipeline:
    def __init__(self):
        self.file = open('femdom_movie.json', 'a', encoding='utf-8')
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)
        return item
    def colse_spider(self):
        self.file.close()


# 小说
class FemdomRedisNovelSlaverPipeline:
    def __init__(self):
        self.file = open('femdom_novel.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)
        return item

    def colse_spider(self):
        self.file.close()