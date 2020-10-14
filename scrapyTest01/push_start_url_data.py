# _*_ coding: utf-8 _*_
# @Time     : 2020/5/1 23:14
# @Author   : Ole211
# @Site     : 
# @File     : push_start_url_data.py    
# @Software : PyCharm

import redis
import json
import requests
import sys

r = redis.Redis(host='192.168.43.249', port=6379)

def push_start_url_data(request_data):
    '''
    将一个完整的request_data 推送到start_url 列表中
    :param request_data: {'url':url, 'form_data':form_data}
    :return:
    '''
    r.lpush('shop168:start_urls', request_data)

def getGoodsTypeList():
    '''
    获取商品id的函数
    :param url: https://www.168.com/sys/getGoodsTypeList
    :return: 返回商品类别的ID列表
    '''
    url = 'https://www.168.com/sys/getGoodsTypeList'
    data = {
        'flag': 1
    }
    res = requests.post(url, data=data)
    goods_type_list = json.loads(res.text)['data']
    return goods_type_list

def getPageNums(goodsfirsttypeid=61):
    '''
    获取某类商品总页码的函数
    :param url:https://www.168.com/buy/GoodsSearchForC
    :param goodsfirsttypeid:
    :return:
    '''
    url = 'https://www.168.com/buy/GoodsSearchForC'
    form_data = {
        'name': '',
        'userid': '',
        'pageNo': '1',
        'pageSize': '20',
        'goodsfirsttypeid': str(goodsfirsttypeid)
    }
    res = requests.post(url, data=form_data)
    pages = json.loads(res.text)['data']['data']['pages']
    return pages

def main(goodsfirsttypeid, pageNo = 1):
    '''
    向redis发送数据data
    :param pageNo:
    :return:
    '''
    url = 'https://www.168.com/buy/GoodsSearchForC/'
    form_data = {
        'name': '',
        'userid': '',
        'pageNo': str(pageNo),
        'pageSize': '20',
        'goodsfirsttypeid': str(goodsfirsttypeid)
    }
    request_data = {
        'url': url,
        'form_data': form_data
    }
    push_start_url_data(json.dumps(request_data))
    print('已经向redis推送数据... %s'%request_data)

if __name__ == '__main__':
    goodsfirsttypeid = getGoodsTypeList()[0]['id']
    page_nums = getPageNums(goodsfirsttypeid)
    print(goodsfirsttypeid, page_nums)
    # main(goodsfirsttypeid, sys.argv[1])