# Импорт библиотеки для работы с SQLite
import sqlite3
import datetime


def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    existing_columns = [column[1] for column in cursor.fetchall()]
    return column_name in existing_columns



# Функция создания таблицы для данных с Центрального банка России (CBRF)
def create_table_cbrf(cursor):
    
    # SQL-запрос для создания таблицы
    sqlite_create_table_cbrf = f"""CREATE TABLE _cbrf (
        indx TEXT NOT NULL UNIQUE PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
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
    
    
# Функция создания таблицы для данных с Центрального банка России (investing_for_graph)
def create_table_investing_for_graph(cursor):
    
    # SQL-запрос для создания таблицы
    create_table_investing_for_graph = f"""CREATE TABLE _investing_for_graph (
        indx TEXT NOT NULL UNIQUE PRIMARY KEY
    )"""
    
    cursor.execute(create_table_investing_for_graph) # Выполнение SQL-запроса
    print("Таблица SQLite _investing_for_graph создана")


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
            
        if not table_exists(cursor, '_investing_for_graph'):
            create_table_investing_for_graph(cursor) # Создание таблицы для Investing.com

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
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        
        if not table_exists(cursor, '_cbrf'):
            create_database()

        new_col = datetime.datetime.now().strftime("col__%d_%m_%y")
        if not column_exists(cursor, '_cbrf', new_col):
            sql_query = f"ALTER TABLE _cbrf ADD COLUMN {new_col} REAL;"
            cursor.execute(sql_query)
        
        for item in data:
            # Обновляем только новый столбец для каждой существующей строки
            update_query = f"UPDATE _cbrf SET {new_col} = ? WHERE indx = ?"
            cursor.execute(update_query, (item[2], item[0]))

        sqlite_connection.commit()
        print("Данные успешно обновлены в таблице _cbrf")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
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
            

# Функция для обновления таблицы с данными Investing.com            
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
            

def insert_data_into_database_investing_for_graph(data):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')  # Устанавливаем соединение с базой данных
        cursor = sqlite_connection.cursor()

        if not table_exists(cursor, '_investing_for_graph'):
            create_database()  # Создаем базу данных и таблицу, если они не существуют

        current_time = datetime.datetime.now().strftime("%d_%m_%y__%H_%M_%S")
        new_col = f"col__{current_time}"

        # Проверяем, существует ли столбец
        if not column_exists(cursor, '_investing_for_graph', new_col):
            # Создаем новый столбец
            cursor.execute(f"ALTER TABLE _investing_for_graph ADD COLUMN {new_col} REAL;")

        # Добавляем данные в новый столбец
        for item in data:
            insert_query = f"""UPDATE _investing_for_graph SET {new_col} = ? WHERE indx = ?"""
            cursor.execute(insert_query, (item[1], item[0]))

        sqlite_connection.commit()  # Сохранение изменений в базе данных
        print("Данные успешно добавлены в таблицу _investing_for_graph")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()  # Закрываем соединение с базой данных
            print("Соединение с SQLite закрыто")
