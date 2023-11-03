import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        

async def cbrf(html):
    soup = BeautifulSoup(html, "lxml")
    return await print("Hello")
    

async def parse_page(url: str, name: str):
    html = await fetch_url(url=url)
    
    states = {
    "https://cbr.ru/curreNcy_base/daily/": cbrf,
    
}
    
    