# -*- coding: utf-8 -*-
import scrapy
import os


class DongmanSpider(scrapy.Spider):
    name = 'dongman'
    allowed_domains = ['m.umei.cc']
    start_urls = ['https://m.umei.cc/katongdongman/dongmantupian/{}.htm'.format(i) for i in range(1, 117)]

    def parse(self, response):
        # links = ['https://m.umei.cc/katongdongman/dongmantupian/{}.htm'.format(i) for i in range(1, 3)]
        img_links = response.xpath('/html/body/div[11]/ul/li/a/img/@data-original').re(r'^http://kr.shaodiyejin.com/file/.*?.jpg$')
        print("*"*30)
        for img_link in img_links:
            item = {}
            item["img_link"] = img_link
            item["img_name"] = os.path.split(img_link)[-1]
            print(item)
            yield item
            