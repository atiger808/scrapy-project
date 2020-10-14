from concurrent.futures import ThreadPoolExecutor, wait
from run_time import run_time as run
from bs4 import BeautifulSoup as bs
import os, json

MAX_WORKERS = os.cpu_count() * 5

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'}

urls = ['https://www.1905.com/vod/list/n_1/o3p{}.html'.format(i) for i in range(1, 100)]


def to_json(item):
    if item:
        with open('film_threadPool.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print(item)


def spider_task(url):
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


@run
def spider():
    executor = ThreadPoolExecutor(5)
    # 使用线程池运行， 运行记过放入列表中
    fs = [executor.submit(spider_task, url) for url in urls]
    # 等待列表中的所有任务都执行完毕
    wait(fs)
    # 销毁线程
    executor.shutdown()


if __name__ == "__main__":
    spider()
