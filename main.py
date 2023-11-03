import asyncio
from pars import parse_page

async def main():
    urls = [
        "https://cbr.ru/curreNcy_base/daily/", 
        "https://ru.investing.com/currencies/single-currency-crosses", 
        "https://finance.rambler.ru/currencies/"
    ]
    tasks = [parse_page(url) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
