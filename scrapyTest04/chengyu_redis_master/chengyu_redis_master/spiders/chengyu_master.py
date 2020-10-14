# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy.spiders import CrawlSpider

class ChengyuMasterSpider(CrawlSpider):
    name = 'chengyu_master'
    # allowed_domains = ['chengyu.t086.com']
    # start_urls = ['http://chengyu.t086.com/list.html']
    def start_requests(self):
        url = 'http://chengyu.t086.com/list.html'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        category = response.xpath('//div[@class="subNav"]/a/@href').re(r'/list/(\w+)_1.html')
        for c in category:
            p = 1
            while True:
                print('=' * 40)
                print(p)
                pageUrl = 'http://chengyu.t086.com/list/{}_{}.html'.format(c, p)
                res = requests.get(pageUrl)
                if res.status_code == 200:
                    yield scrapy.Request(pageUrl, callback=self.parse_page)
                else:
                    break
                p = p + 1

    def parse_page(self, response):
        item_links = response.xpath('//div[@class="listw"]/ul/li/a/@href').re(r'/cy\d+/\d+.html')
        item_links = ['http://chengyu.t086.com' + i for i in item_links]
        for item_link in item_links:
            item = {}
            item['url'] = item_link
            print(item)
            yield item
