import os
import pandas as pd
from sqlalchemy import create_engine

# Путь к базе данных SQLite
db_path = os.path.join('api_yamdb', 'db.sqlite3')

# Создаем подключение к базе данных SQLite
engine = create_engine(f'sqlite:///{db_path}')

# Путь к директории с CSV-файлами
csv_directory = os.path.join('api_yamdb', 'static', 'data')

# Перебираем все файлы в директории
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        # Полный путь к CSV-файлу
        file_path = os.path.join(csv_directory, filename)
        
        # Чтение CSV-файла в DataFrame
        df = pd.read_csv(file_path)
        
        # Имя таблицы в базе данных с префиксом 'reviews_'
        table_name = 'reviews_' + os.path.splitext(filename)[0]
        
        # Запись данных в таблицу
        df.to_sql(table_name, engine, index=False, if_exists='replace')

        print(f"Импортирован файл {filename} в таблицу {table_name}")