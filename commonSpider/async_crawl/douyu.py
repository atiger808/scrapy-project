from run_time import run_time as run
from lxml import etree
import asyncio
import aiohttp
headers = {
    # 请求的来源网页
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'
}
urls = [f'https://www.doutula.com/article/list/?page={p}' for p in range(1, 2)]

async def get(url):
    async with aiohttp.ClientSession(
            headers=headers, connector = aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as res:
            return await res.text()

async def save_img(src):
    headers['Referer'] = 'http://www.doutula.com/'
    async with aiohttp.ClientSession(
            headers=headers, connector = aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(src) as res:
            return await res.content

async def douyuspidder():
    tasks = [get(url) for url in urls]
    pages = await asyncio.gather(*tasks)
    for page in pages:
        html = etree.HTML(page)
        srcs = html.xpath('//img/@data-original')
        for src in srcs:
            filename = src.split('/')[-1]
            print(src, filename)
            content = save_img(src)
            print(len(content))



@run
def main():
    asyncio.run(douyuspidder())

if __name__ == '__main__':
    main()