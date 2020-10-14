# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re, os

class FemdomNovelMasterSpider(CrawlSpider):
    name = 'femdom_novel_master'
    allowed_domains = ['qsead.cc']
    # start_urls = ['https://qsead.cc/?t=fiction/index']
    rules = (
        Rule(LinkExtractor(allow=r'https://qsead.cc/?t=fiction/index&p=\d+&c=&s='), callback='parse_item', follow=True),
    )

    def start_requests(self):
        url = 'https://qsead.cc/?t=fiction/index'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        html = response.xpath('//li[@class="other other-4"]/a/@href').re(r'\?t=fiction/index&p=(\d+)&c=&s=')
        nums = int(html[0])
        print(nums)
        for p in range(1, nums+1):
            pageUrl = 'https://qsead.cc/?t=fiction/index&p={}&c=&s='.format(p)
            yield scrapy.Request(pageUrl, callback=self.parse_item)


    def parse_item(self, response):
        item = {}
        links = response.xpath('//div[@class="list"]/div[@class="box"]//a[@class="info"]/@href').re('\?t=fiction/content&md5=.*')
        links = [os.path.join('https://qsead.cc/', i) for i in links]
        for i in links:
            item['url'] = i
            print(item)
            yield item