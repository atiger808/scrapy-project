# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
import scrapy
import re, json
import urllib.parse
from ..items import FemdomRedisSlaverItem

class FemdomSlaverSpider(RedisCrawlSpider):
    name = 'femdom_slaver'
    # allowed_domains = ['qsead.cc']
    # start_urls = ['https://www.qsead.cc/']
    redis_key = 'femdom:start_urls'
    page_links = LinkExtractor(allow=r'https://www.qsead.cc/?t=video/index&p=\d+&class=.*?&s=')
    # movie_links = LinkExtractor(allow=r'\?t=video/play&id=.*?', restrict_xpaths=('*//a[@class="info"]/@href'))
    rules = (
        Rule(page_links, callback='parse', follow=True),
        # Rule(movie_links)
    )
    def __init__(self):
        self.category = None
    def parse(self, response):
        self.category = response.url.split('class=')[-1]
        links = response.xpath('*//a[@class="info"]/@href').extract()
        links = ['https://www.qsead.cc/'+i for i in links]
        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)
    def parse_item(self, response):
        item = FemdomRedisSlaverItem()
        item['id'] = response.url.split('id=')[-1]
        item['url'] = response.url
        item['title'] = response.xpath('*//h1[@id="Video-Title"]//text()').extract()[0]
        print('='*40)
        item['source'] = response.xpath('//video[@id="Play_Tag"]/@src').extract()[0]
        item['poster'] = response.xpath('//video[@id="Play_Tag"]/@poster').extract()[0]+'cover.jpg'
        item['category'] = urllib.parse.unquote(self.category.strip('&s='))
        print(item)
        yield item
