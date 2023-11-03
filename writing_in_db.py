import sqlite3

def create_table_cbrf(cursor):
    sqlite_create_table_cbrf = """CREATE TABLE _cbrf (
        indx TEXT NOT NULL UNIQUE PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        value REAL NOT NULL
    )"""
    
    cursor.execute(sqlite_create_table_cbrf)
    print("Таблица SQLite _cbrf создана")

def create_table_rambler(cursor):
    sqlite_create_table_rambler = """CREATE TABLE _rambler (
        indx TEXT NOT NULL UNIQUE PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        value REAL NOT NULL,
        change REAL NOT NULL,
        increase TEXT NOT NULL
    )"""
    
    cursor.execute(sqlite_create_table_rambler)
    print("Таблица SQLite _rambler создана")
    
def create_table_investing(cursor):
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
        
    cursor.execute(sqlite_create_table_investing)
    print("Таблица SQLite _investing создана")

def create_database():
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()

        if not table_exists(cursor, '_cbrf'):
            create_table_cbrf(cursor)

        if not table_exists(cursor, '_rambler'):
            create_table_rambler(cursor)
            
        if not table_exists(cursor, '_investing'):
            create_table_investing(cursor)

        sqlite_connection.commit()
        print("Таблицы созданы")

    except sqlite3.Error as error:
        print("Ошибка при создании таблицы:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    result = cursor.fetchone()
    return result is not None

# Остальной код остается без изменений

def insert_data_into_database_cbrf(data):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()

        if not table_exists(cursor, '_cbrf'):
            create_database()

        for item in data:
            insert_query = """INSERT OR REPLACE INTO _cbrf (indx, name, value) VALUES (?, ?, ?)"""
            cursor.execute(insert_query, item)

        sqlite_connection.commit()
        print("Данные успешно добавлены в таблицу")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def insert_data_into_database_rambler(data):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()

        if not table_exists(cursor, '_rambler'):
            create_database()

        for item in data:
            insert_query = """INSERT OR REPLACE INTO _rambler (indx, name, value, change, increase) VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(insert_query, item)

        sqlite_connection.commit()
        print("Данные успешно добавлены в таблицу _rambler")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
            
            
def insert_data_into_database_investing(data):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()

        if not table_exists(cursor, '_investing'):
            create_database()

        for item in data:
            insert_query = """INSERT OR REPLACE INTO _investing (indx, demand, supply, max, min, change, increase, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(insert_query, item)

        sqlite_connection.commit()
        print("Данные успешно добавлены в таблицу _investing")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
