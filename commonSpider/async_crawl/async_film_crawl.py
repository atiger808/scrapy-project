from run_time import run_time as run
from bs4 import BeautifulSoup as bs
import os, json
import asyncio
import aiohttp

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'}

urls = ['https://www.1905.com/vod/list/n_1/o3p{}.html'.format(i) for i in range(1, 100)]


def to_json(item):
    if item:
        with open('film_async.json', 'a', encoding='utf-8') as f:
            print(item)
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


async def get(url):
    async with aiohttp.ClientSession(
            headers=headers, connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as res:
            return await res.text()


async def spider():
    tasks = [get(url) for url in urls]
    pages = await asyncio.gather(*tasks)
    for page in pages:
        soup = bs(page, 'html.parser')
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
def main():
    asyncio.run(spider())


if __name__ == "__main__":
    main()
