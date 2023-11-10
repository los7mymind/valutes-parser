# Импорт необходимых библиотек и модулей
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from writing_in_db import insert_data_into_database_cbrf, insert_data_into_database_rambler, insert_data_into_database_investing, insert_data_into_database_investing_for_graph


# Функция для асинхронного получения HTML-кода страницы по URL-адресу
async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        

# Функция для парсинга данных о валюте с Центрального банка России (CBRF)
async def cbrf(html, soup):
    temp = soup.find_all("tr", class_="")
    data_to_insert = []
    for item in temp[1:]:
        item = item.text.strip().split('\n')
        item[4] = float(item[4].replace(',', '.')) / float(item[2])
        data_to_insert.append((item[1], item[3], item[4]))
    insert_data_into_database_cbrf(data_to_insert)


# Функция для парсинга данных о валюте с ресурса "Rambler"
async def rambler(html, soup):
    temp = soup.find_all("a", class_="finance-currency-table__tr")
    data_to_insert = []
    for item in temp:
        item = [i for i in item.text.strip().split('\n') if i != ""]
        item[3] = float(item[3]) / float(item[1])
        item[4] = float(item[4].replace('–', '-')) / float(item[1])
        data_to_insert.append((item[0], item[2], item[3], item[4], item[5]))
    insert_data_into_database_rambler(data_to_insert)


# Функция для парсинга данных о валюте с ресурса "Investing.com"
async def investing(html, soup):
    temp = soup.find_all("tr", class_="datatable_row__Hk3IV dynamic-table_row__fdxP8")
    
    data_to_insert = []
    data_to_insert_for_graph_table = []
    
    for item in temp:
        data = item.stripped_strings
        data_list = list(data)
        data_to_insert.append(data_list)
        data_to_insert_for_graph_table.append((data_list[0], data_list[2]))
    insert_data_into_database_investing(data_to_insert)
    insert_data_into_database_investing_for_graph(data_to_insert_for_graph_table)
    


# Функция для асинхронного выполнения парсинга данных для указанного URL-адреса
async def parse_page(url: str):
    while True:
        html = await fetch_url(url=url) # Получаем HTML-код страницы
        soup = BeautifulSoup(html, "lxml") # Создаем объект BeautifulSoup для парсинга HTML

        
        # Определяем, какую функцию вызывать в зависимости от URL
        if url == "https://cbr.ru/curreNcy_base/daily/":
            await cbrf(html=html, soup=soup)
        elif url == "https://ru.investing.com/currencies/single-currency-crosses":
            await investing(html=html, soup=soup)
        elif url == "https://finance.rambler.ru/currencies/":
            await rambler(html=html, soup=soup)

        await asyncio.sleep(60) # Ожидание перед следующим запросом
   
    