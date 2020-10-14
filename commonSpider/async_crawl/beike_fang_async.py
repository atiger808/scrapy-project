import requests
from bs4 import BeautifulSoup as bs
import re, json
import asyncio
import aiohttp

from run_time import run_time as run
ershou_urls = [f'https://m.ke.com/xc/ershoufang/pg{i}' for i in range(1, 100)]

new_url = 'https://m.ke.com/xc/loupan/fang/'


def save_json(item):
    if item:
        with open('ershou_beike.json', 'a', encoding='utf-8') as f:
            content = json.dumps(item, ensure_ascii=False) + '\n'
            f.write(content)
        print('success')

async def get(url):
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as res:
            return await res.text()
    
        
async def spider():
    tasks = [get(url) for url in ershou_urls]
    pages = await asyncio.gather(*tasks)
    for page in pages:
        soup = bs(page, 'html.parser')
        li = soup.findAll('a', href=re.compile('https://m.ke.com/xc/ershoufang/.*?fb_expo_id=.*?'))
        for i in li:
            item = {}
            item['url'] = i.get('href')
            item['title'] = i.find('div', class_='house-title').text
            item['desc'] = i.find('div', class_='house-desc').text
            item['price_total'] = i.find('span', class_='price-total').text
            item['price_unit'] = i.find('span', class_='price-unit').text
            save_json(item)
    
@run
def main():
    asyncio.run(spider())
    
    
main()