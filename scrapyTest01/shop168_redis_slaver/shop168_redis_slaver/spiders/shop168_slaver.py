# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
import scrapy
import re, json
from selenium import webdriver
from shop168_redis_slaver.items import Shop168RedisSlaverItem

class Shop168SlaverSpider(RedisCrawlSpider):
    name = 'shop168_slaver'
    # allowed_domains = ['168.com']
    # start_urls = ['http://168.com/']
    redis_key = 'shop168:start_urls'
    # rules = (
    #     Rule(LinkExtractor(allow=r'buy/GoodsSearchForC/'), callback='parse_item', follow=True),
    # )

    def make_request_from_data(self, data):
        data = json.loads(data)
        url = data.get('url')
        form_data = data.get('form_data')
        return scrapy.FormRequest(url=url, formdata=form_data, callback=self.parse_item)

    def parse_item(self, response):
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        res = response.body.decode('utf-8')
        res = json.loads(res)['data']['data']['list']
        for i in res:
            item = {}
            item['name'] = i['goodsName']
            item['price'] = i['minPrice']
            item['link'] = 'https://www.168.com/common/GoodsDetail.html?goodsid='+str(i['id'])
            item['pic'] = 'https://www.168.com/images/'+i['mainpic']
            print(item)
            print('#'*30)
            yield item
