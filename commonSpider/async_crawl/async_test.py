import asyncio
import functools
from run_time import run_time as run
from aiohttp import ClientSession
import aiohttp
import concurrent.futures

from bs4 import BeautifulSoup as bs
import requests
import os, json

MAX_WORKERS = os.cpu_count() * 5

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'}

urls = ['https://www.1905.com/vod/list/n_1/o3p{}.html'.format(i) for i in range(1, 100)]


def to_json(item):
    if item:
        with open('film.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print(item)


def parse_item(url):
    res = requests.get(url, headers=headers)
    soup = bs(res.text, 'html.parser')
    li = soup.find(class_='mod row search-list').findAll('div')
    for i in li:
        item = {}
        item['title'] = i.find('a').get('title')
        item['poster'] = i.find('img').get('src')
        url = i.find('a').get('href')
        item['id'] = os.path.splitext(os.path.split(url)[-1])[0]
        item['summary'] = i.find('p').text
        score = i.find(class_='score')
        if score:
            item['score'] = score.text.strip()
        else:
            item['score'] = ''
        to_json(item)


def load_url(url):
    res = requests.get(url)
    return res.text


def threadPool():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(parse_item, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as e:
                print("%s generate an exception: %s" % (url, e))
            print("正在下载: %s" % (url))


# 下载协程
async def download(url):
    # await asyncio.sleep(1)
    async with ClientSession(
            headers=headers, connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as res:
            print('正在下载: ', url)
            return await res.text()


# 回调函数
def on_finish(url, task):
    print("下载完成: ", url, task.result(), task.exception())


# 调度协程    
async def schedule():
    for url in urls:
        # 创建协程对象
        co = download(url)
        # 包装成task
        task = asyncio.create_task(co)
        # 设置完成会掉回调函数
        task.add_done_callback(functools.partial(on_finish, url))
        await asyncio.sleep(0)


@run
def main():
    threadPool()

    # asyncio.run(schedule())


if __name__ == "__main__":
    # urls = ["https://www.baidu.com/" for _ in range(100)]
    main()
