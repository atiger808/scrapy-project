# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChengyuRedisSlaverItem(scrapy.Item):
    # define the fields for your item here like:
    # utc时间
    crawled = scrapy.Field()
    # 爬虫名称
    spider = scrapy.Field()

    # 成语信息
    # 名称
    title = scrapy.Field()
    # 发音
    pronounce = scrapy.Field()
    # 释义
    paraphrase = scrapy.Field()
    # 出处
    reference = scrapy.Field()
    # 人气
    influence = scrapy.Field()
    # 百度百科链接
    link = scrapy.Field()
