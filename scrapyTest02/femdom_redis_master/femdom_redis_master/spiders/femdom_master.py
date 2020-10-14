# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re, json
class FemdomMasterSpider(CrawlSpider):
    name = 'femdom_master'
    allowed_domains = ['qsead.cc']
    # start_urls = ['https://www.qsead.cc/?t=video/index']
    # rules = (
    #     Rule(LinkExtractor(allow=r't=video/index$'), callback='parse', follow=True),
    # )

    def start_requests(self):
        url = 'https://www.qsead.cc/?t=video/index'
        yield scrapy.Request(url, callback=self.parse)

    # 获取视频首页各种视频类别的链接
    def parse(self, response):
        links = response.xpath('//div[@class="row"]/a/@href').re(r'\?t=video/index&p=\d+&class=.+')
        links = ['https://www.qsead.cc/'+i for i in links]
        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)

    # 获取每个类别视频页数的链接, 并写入redis
    def parse_item(self, response):
        print('=='*30)
        res = response.body.decode('utf-8')
        print(response.url)
        pattern = r'other other-4"><a href="\?t=video/index&p=(\d+)&'
        r = re.search(pattern, res)
        category = response.url.split('class=')[-1]
        pageNum = int(r.group(1))
        print(pageNum)
        for p in range(1, pageNum+1):
            item = {}
            url = 'https://www.qsead.cc/?t=video/index&p={}&class={}'.format(p, category)
            item['url'] = url
            print(item)
            yield item
