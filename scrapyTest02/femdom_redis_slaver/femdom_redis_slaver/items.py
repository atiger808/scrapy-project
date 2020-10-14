# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FemdomRedisSlaverItem(scrapy.Item):
    # define the fields for your item here like:
    # utc 时间
    crawled = scrapy.Field()
    # 爬虫名
    spider = scrapy.Field()
    title = scrapy.Field()
    id = scrapy.Field()
    source = scrapy.Field()
    poster = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()

class FemdomRedisNovelSlaverItem(scrapy.Item):
    # utc 时间
    crawled = scrapy.Field()
    # 爬虫名
    spider = scrapy.Field()

    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    articleId = scrapy.Field()
