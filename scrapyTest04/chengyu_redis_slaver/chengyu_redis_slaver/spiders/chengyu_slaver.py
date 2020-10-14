# -*- coding: utf-8 -*-
import scrapy
import re
import requests
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import  Rule
from scrapy.linkextractors import LinkExtractor
class ChengyuSlaverSpider(RedisCrawlSpider):
    name = 'chengyu_slaver'
    redis_key = 'chengyu:start_urls'
    # page_link = LinkExtractor(allow=r'http://chengyu.t086.com/cy\d+/\d+.html')
    # rules = (
    #     Rule(page_link, callback='parse', follow=True),
    # )

    def parse(self, response):
        print('#'*40)
        item = {}
        table = response.xpath('//div[@id="main"]/table').get()
        table = table.replace('\n', '')
        pattern = r'<td class="t" width="15%">词目</td>'\
                  +'<td><h1>(.*?)</h1></td>'\
                  +'.*?发音</td>'\
                  +'<td>(.*?)</td>'\
                  +'.*?释义</td>'\
                  +'<td>(.*?)</td>'\
                  +'.*?出处</td>'\
                  +'<td>(.*?)</td>'\
                  +'.*?人气</td>'\
                  +'<td><span id="hits">(\d+)</span>次</td>'\
                  +'.*?相关</td>'\
                  +'<td class="t2"><a href="(.*?)" target="_blank">'

        data = re.findall(pattern, table, re.S)
        print('~'*40)
        if data:
            data = data[0]
            item['title'] = data[0]
            item['pronounce'] = data[1]
            item['paraphrase'] = data[2]
            item['reference'] = data[3]
            item['influence'] = int(data[4])
            item['link'] = data[5]
            print(item)
            yield item
        else:
            print('empty!')
            print(response.url)
