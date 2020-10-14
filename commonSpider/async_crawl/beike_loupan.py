import requests
from bs4 import BeautifulSoup as bs
import re, json
import asyncio
import aiohttp

from run_time import run_time as run


base_url = 'https://m.ke.com'
new_urls = ['https://m.ke.com/xc/loupan/fang/pg{}'.format(i) for i in range(1, 19)]


async def get(url):
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as res:
            return await res.text()
    

async def get_links():
    tasks = [get(url) for url in new_urls]
    pages = await asyncio.gather(*tasks)
    total_links = []
    for page in pages:
        soup = bs(page, 'html.parser')
        links = soup.findAll('a', href=re.compile('https://m.ke.com/xc/loupan/p_.*?'))
        links = [i.get('href') for i in links]
        total_links.extend(links)
    return total_links


def save_json(item):
    if item:
        with open('loupan_beike.json', 'a', encoding='utf-8') as f:
            content = json.dumps(item, ensure_ascii=False) + '\n'
            f.write(content)
        # print('success')

async def spider():
    global total_urls
    tasks = [get(url) for url in total_urls]
    pages = await asyncio.gather(*tasks)
    for page in pages:
        try:  
            soup = bs(page, 'html.parser')
            info = soup.find('div', class_='price-and-address-wrapper change-price-address')
            item = {}
            title = soup.find('h1')
            if title:
                item['title'] = title.text
            else:
                title= soup.find('title')
                if title:
                    item['title'] = title
                else:
                    item['title'] = "暂无"
            
            item['price'] = info.find('span', class_='price-value item').text
            desc = info.findAll(class_='address-value item')
            if desc:
                item['area'] = desc[0].text
                item['types'] = desc[1].text
                item['struct'] = desc[2].text
            date= info.find('div', class_='address-value item post_ulog')
            if date:
                item['date'] = date.text
            else:
                item['date'] = '暂无'
            address = info.find('a', class_='address-value item new_post_ulog')
            if address:
                item['address'] = address.text
                item['pos_url'] = base_url+address.get('href')
            else:
                item['pos_url'] = '暂无'
                address = info.find('div', class_='normal-value normal item')
                if address is None:
                    item['address'] = '暂无'
                else:
                    item['address'] = address.text
            save_json(item)
        except Exception as e:
            print(e)
            print(item['title'])
            break



@run
def main():
    global total_urls
    total_urls = asyncio.run(get_links())
    print(len(total_urls))
    asyncio.run(spider())
    


main()