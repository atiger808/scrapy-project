# _*_ coding: utf-8 _*_
# @Time     : 2020/6/10 0:31
# @Author   : Ole211
# @Site     : 
# @File     : submitData.py    
# @Software : PyCharm

import requests
import json
import pandas as pd
from run_time import run_time as run
import threading


def json2csv():
    with open(r'd:/json/femdom_movie.json', 'r', errors='ignore', encoding='utf-8') as f:
        content = f.readlines()
    data = [json.loads(i) for i in content]
    df = pd.DataFrame(data)
    df.to_csv(r'd:/json/femdom_movie.csv')
    print(df.head())
    print(len(df.drop_duplicates('id')))
    print(len(df))


def post_data(startPage, endPage):
    global df
    url = 'http://192.168.43.249:8000/article/add_video/'
    for i in range(startPage, endPage):
        print(i)
        data={
            'videoId': df.id[i],
            'title': df.title[i],
            'poster': df.poster[i],
            'url': df.url[i],
            'source':df.source[i],
            'tag':df.category[i]
        }
        res = requests.post(url, data=data)
        print(res.status_code)
        print(res.text)

@run
def threading_run(startPage, endPage, patch=10):
    step = (endPage - startPage) // patch
    start = startPage
    end = startPage + step
    li = []
    for i in range(patch):
        li.append([start, end])
        start = start + step
        end = end + step
    li[-1][-1] = endPage + 1
    threads = [threading.Thread(target=post_data, args=(offset[0], offset[1]), ) for offset in li]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

@run
def main():
    df = pd.read_csv(r'D:\json\femdom_movie.csv')
    print(df.columns)
    print(len(df))
    post_data(0, 200)
    # threading_run(0, 200)

if __name__ == '__main__':
    # json2csv()

    df1 = pd.read_csv(r'D:\json\femdom_movie-pi.csv')
    df2 = pd.read_csv(r'D:\json\femdom_movie-win.csv')
    print(len(df1))
    print(len(df2))
    print(len(df1)+len(df2))



