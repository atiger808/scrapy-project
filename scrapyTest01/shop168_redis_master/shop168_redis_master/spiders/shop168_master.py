# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json


class Shop168MasterSpider(CrawlSpider):
    name = 'shop168_master'
    # allowed_domains = ['168.com']
    # start_urls = ['http://168.com/']
    start_urls = ['https://www.168.com/buy/GoodsSearchForC/', 'https://www.168.com/sys/getGoodsTypeList']

    rules = (
        Rule(LinkExtractor(allow=r'/buy|sys\w*/'), callback='parse_item', follow=True),
    )

    def __init__(self):
        self.goods_type_list = None

    def start_requests(self):
        '''
        # 首先获取商品的类型id
        url :'https://www.168.com/sys/getGoodsTypeList'
        :return:
        '''
        data = {
            'flag': '1'
        }
        yield scrapy.FormRequest(url=self.start_urls[1], formdata=data, callback=self.parse)

    def parse(self, response):
        '''
        # 其次爬取某一类型商品数据
        url: 'https://www.168.com/buy/GoodsSearchForC/'
        :param reponse:
        :return:
        '''
        goods_type_list = json.loads(response.body)['data']
        self.goods_type_list =goods_type_list
        form_data = {
            'name': '',
            'userid': '',
            'pageNo': '1',
            'pageSize': '20',
            'goodsfirsttypeid': str(self.goods_type_list[0]['id'])
        }
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=form_data, callback=self.parse_item)

    def parse_item(self, response):
        item = {}
        for goods in self.goods_type_list[10:]:
            form_data = {
                'name': '',
                'userid': '',
                'pageNo': '1',
                'pageSize': '20',
                'goodsfirsttypeid': str(goods['id'])
            }
            scrapy.FormRequest(url=self.start_urls[0], formdata=form_data)
            data = response.body.decode('utf-8')
            pageNums = json.loads(data)['data']['data']['pages']

            print('####################')
            print(goods['id'])
            print('####################')

            for pageNo in range(1, int(pageNums)):
                print('---------------------')
                print('    %s' % pageNo)
                print('---------------------')

                form_data = {
                    'name': '',
                    'userid': '',
                    'pageNo': str(pageNo),
                    'pageSize': '20',
                    'goodsfirsttypeid': str(goods['id'])
                }
                request_data = {
                    'url': self.start_urls[0],
                    'form_data': form_data
                }
                item['url'] = json.dumps(request_data)
                print(item)
                yield item

