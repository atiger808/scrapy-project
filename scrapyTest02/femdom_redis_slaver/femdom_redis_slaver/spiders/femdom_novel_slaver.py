# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from ..items import FemdomRedisNovelSlaverItem
import re, json

class FemdomNovelSlaverSpider(RedisCrawlSpider):
    name = 'femdom_novel_slaver'
    # allowed_domains = ['qsead.cc']
    # start_urls = ['http://qsead.cc/']
    redis_key = 'femdom_novel:start_urls'
    page_links = LinkExtractor(allow=r'https://www.qsead.cc/?t=fiction/content&md5=.*?')
    rules = (
        Rule(page_links, callback='parse', follow=True),
    )

    def parse(self, response):
        item = FemdomRedisNovelSlaverItem()
        item['title'] = response.xpath('//div[@class="title-box"]/h1/text()').get()
        article = response.xpath('//div[@class="content"]/p/text()').extract()
        item['content'] = '||'.join(p for p in article)
        item['url'] = response.url
        item['articleId'] = response.url.split('md5=')[-1]
        print('='*40)
        print(response.url)
        yield item