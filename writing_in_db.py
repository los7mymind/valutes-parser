# Импорт библиотеки для работы с SQLite
import sqlite3


# Функция создания таблицы для данных с Центрального банка России (CBRF)
def create_table_cbrf(cursor):
    
    # SQL-запрос для создания таблицы
    sqlite_create_table_cbrf = """CREATE TABLE _cbrf (
        indx TEXT NOT NULL UNIQUE PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        value REAL NOT NULL
    )"""
    
    cursor.execute(sqlite_create_table_cbrf) # Выполнение SQL-запроса
    print("Таблица SQLite _cbrf создана")


# Функция создания таблицы для данных с ресурса "Rambler"
def create_table_rambler(cursor):
    
    # SQL-запрос для создания таблицы
    sqlite_create_table_rambler = """CREATE TABLE _rambler (
        indx TEXT NOT NULL UNIQUE PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        value REAL NOT NULL,
        change REAL NOT NULL,
        increase TEXT NOT NULL
    )"""
    
    cursor.execute(sqlite_create_table_rambler) # Выполнение SQL-запроса
    print("Таблица SQLite _rambler создана")


# Функция создания таблицы для данных с ресурса "Investing"
def create_table_investing(cursor):
    
    # SQL-запрос для создания таблицы
    sqlite_create_table_investing = """CREATE TABLE _investing (
        indx TEXT NOT NULL UNIQUE PRIMARY KEY,
        demand TEXT NOT NULL,
        supply TEXT NOT NULL,
        max TEXT NOT NULL,
        min TEXT NOT NULL,
        change TEXT NOT NULL,
        increase TEXT NOT NULL,
        time TEXT NOT NULL
        )"""
        
    cursor.execute(sqlite_create_table_investing) # Выполнение SQL-запроса
    print("Таблица SQLite _investing создана")


# Функция для создания базы данных
def create_database():
    
    # Создание таблиц
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db') # Устанавливаем соединение с базой данных
        cursor = sqlite_connection.cursor()

        # Проверка на наличие таблиц в базе данных
        if not table_exists(cursor, '_cbrf'):
            create_table_cbrf(cursor) # Создание таблицы для CBRF

        if not table_exists(cursor, '_rambler'):
            create_table_rambler(cursor) # Создание таблицы для Rambler
            
        if not table_exists(cursor, '_investing'):
            create_table_investing(cursor) # Создание таблицы для Investing.com

        sqlite_connection.commit() # Сохранение изменений
        print("Таблицы созданы")

    except sqlite3.Error as error:
        print("Ошибка при создании таблицы:", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close() # Закрываем соединение с базой данных
            print("Соединение с SQLite закрыто")


# Функция для проверки на наличие таблицы в базе данных
def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    result = cursor.fetchone()
    return result is not None


# Функция для обновления таблицы с данными Центрального банка России (cbrf)
def insert_data_into_database_cbrf(data):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db') # Устанавливаем соединение с базой данных
        cursor = sqlite_connection.cursor()

        if not table_exists(cursor, '_cbrf'):
            create_database() # Создаем базу данных и таблицу, если они не существуют

        for item in data:
            insert_query = """INSERT OR REPLACE INTO _cbrf (indx, name, value) VALUES (?, ?, ?)"""
            cursor.execute(insert_query, item) # Вставляем данные в таблицу

        sqlite_connection.commit() # Сохранение изменений в базе данных
        print("Данные успешно добавлены в таблицу")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close() # Закрываем соединение с базой данных
            print("Соединение с SQLite закрыто")


# Функция для обновления таблицы с данными Rambler
def insert_data_into_database_rambler(data):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db') # Устанавливаем соединение с базой данных
        cursor = sqlite_connection.cursor()

        if not table_exists(cursor, '_rambler'):
            create_database() # Создаем базу данных и таблицу, если они не существуют

        for item in data:
            insert_query = """INSERT OR REPLACE INTO _rambler (indx, name, value, change, increase) VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(insert_query, item) # Вставляем данные в таблицу

        sqlite_connection.commit() # Сохранение изменений в базе данных
        print("Данные успешно добавлены в таблицу _rambler")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close() # Закрываем соединение с базой данных
            print("Соединение с SQLite закрыто")
            
            
def insert_data_into_database_investing(data):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db') # Устанавливаем соединение с базой данных
        cursor = sqlite_connection.cursor()

        if not table_exists(cursor, '_investing'):
            create_database() # Создаем базу данных и таблицу, если они не существуют

        for item in data:
            insert_query = """INSERT OR REPLACE INTO _investing (indx, demand, supply, max, min, change, increase, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(insert_query, item) # Вставляем данные в таблицу

        sqlite_connection.commit() # Сохранение изменений в базе данных
        print("Данные успешно добавлены в таблицу _investing")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close() # Закрываем соединение с базой данных
            print("Соединение с SQLite закрыто")
