# _*_ coding: utf-8 _*_
# @Time     : 2020/5/2 4:01
# @Author   : Ole211
# @Site     : 
# @File     : start_feed_url.py    
# @Software : PyCharm
import os, time
import random
from push_start_url_data import getGoodsTypeList,getPageNums
goodsfirsttypeid = getGoodsTypeList()[0]['id']
page_nums = getPageNums(goodsfirsttypeid)


#
for i in range(1, page_nums):
    os.system('python ./push_start_url_data.py %s'%i)