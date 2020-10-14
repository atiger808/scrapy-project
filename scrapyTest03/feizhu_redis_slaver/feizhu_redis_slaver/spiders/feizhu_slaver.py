# -*- coding: utf-8 -*-
import scrapy
import json


class FeizhuSlaverSpider(scrapy.Spider):
    name = 'feizhu_slaver'

    allowed_domains = ['fliggy.com']
    # start_urls = ['https://fliggy.com/']
    start_urls = ['https://hotel.fliggy.com/ajax/ajaxKezhanList.htm?pageSize=20&currentPage=2&totalItem=5576&startRow=0&endRow=19&city=330100']

    def __init__(self):
        self.dic = {}
    def parse(self, response):
        res = response.body.decode('gbk')
        data = json.loads(res)
        pageNums = int(data['total'])//20+1
        print(pageNums)
        for p in range(1, 2):
            page_url = 'https://hotel.fliggy.com/ajax/ajaxKezhanList.htm?pageSize=20&currentPage={}&totalItem=5576&startRow=0&endRow=19&city=330100'.format(p)
            yield scrapy.Request(page_url, callback=self.parse_page)

    def parse_page(self, response):
        res = response.body.decode('gbk')
        data = json.loads(res)['hotelList']
        shop_list = []
        for i in data:
            self.dic = {}
            self.dic['shid'] = i['shid']
            self.dic['name'] = i['name']
            self.dic['address'] = i['address']
            self.dic['priceDesp'] = i['priceDesp']
            self.dic['lat'] = i['lat']
            self.dic['lng'] = i['lng']
            self.dic['detail_url'] = 'https://hotel.fliggy.com/hotel_detail2.htm?shid={}&city=330100&checkIn=2020-06-24&checkOut=2020-06-25&hotelType=kezhan&_output_charset=utf8'.format(str(self.dic['shid']))
            yield scrapy.Request(self.dic['detail_url'], callback=self.parse_item)

    def parse_item(self, response):
        print(response.body.decode('gbk'))
        # res = response.xpath('//*[@id="hotel-desc"]/div[2]/text()').extract()
        # print(self.dic)
        # print(res)
        print('=' * 40)

