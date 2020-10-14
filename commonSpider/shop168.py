# _*_ coding: utf-8 _*_
# @Time     : 2020/5/1 22:19
# @Author   : Ole211
# @Site     : 
# @File     : shop168.py    
# @Software : PyCharm

import requests
import json

url = 'https://www.168.com/buy/GoodsSearchForC'

headers = {
'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/81.0.4044.129 Mobile Safari/537.36'
}
data = {
    'name': '',
    'pageNo': '2'
}

res = requests.post(url, data=data, headers=headers)
print(res.json())