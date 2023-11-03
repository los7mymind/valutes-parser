from pars import *


async def main():
    urls = ["https://cbr.ru/curreNcy_base/daily/", ]
    tasks = [parse_page(url) for url in urls]
    await asyncio.gather(*tasks)
    
    
    
if __name__ == "__main__":
    asyncio.run(main())