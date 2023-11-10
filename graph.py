import matplotlib.pyplot as plt
import sqlite3

def format_datetime(datetime_str):
    if datetime_str.startswith('col__'):
        # Убираем 'col__' и разделяем строку на части
        parts = datetime_str[5:].split('__')
        if len(parts) == 2:
            # Разделяем части на дату и время
            date_part, time_part = parts
            # Преобразуем дату и время в нужный формат
            formatted_date = '.'.join(date_part.split('_'))  # Преобразуем дату в 'dd.mm.yy'
            formatted_time = ':'.join(time_part.split('_'))  # Преобразуем время в 'hh:mm:ss'
            return f"{formatted_time} - {formatted_date}"
    return datetime_str  # Возвращаем исходное название, если формат не соответствует


def get_row_data(cursor, indx_value):
    try:
        cursor.execute("SELECT * FROM _investing_for_graph WHERE indx = ?", (indx_value,))
        row_data = cursor.fetchone()
        return row_data
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        return None


def get_column_names(cursor, table_name):
    try:
        cursor.execute(f"PRAGMA table_info({table_name});")
        # Получаем только имена столбцов
        columns = [column_info[1] for column_info in cursor.fetchall()]
        return columns
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        return []
    

# Подключаемся к базе данных и получаем данные
sqlite_connection = sqlite3.connect('sqlite_python.db')
cursor = sqlite_connection.cursor()

indx_value = 'EUR/USD'
row_data = get_row_data(cursor, indx_value)
column_names = get_column_names(cursor, '_investing_for_graph')

# Закрываем соединение с базой данных
sqlite_connection.close()

if row_data and column_names:
    # Исключаем первый элемент ('indx') и преобразуем формат даты и времени
    dates = [format_datetime(col_name) for col_name in column_names[1:]]
    values = [float(value.replace(',', '.')) for value in row_data[1:]]

    # Строим график
    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o')
    plt.xticks(rotation=45)
    plt.title('Курс EUR/USD')
    plt.xlabel('Дата и время')
    plt.ylabel('Курс')
    plt.tight_layout()
    plt.show()
else:
    print("Не удалось получить данные для построения графика")