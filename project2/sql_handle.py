from site_data import *
import configuration as conf
import os
import sqlite3

class sql_handler():
    def __init__(self) -> None:
        home_path = os.path.expanduser('~')
        sql_path = f'{home_path}/{conf.sql_folder}'
        self.database_path = f'{sql_path}/database.db'
        self.connection = sqlite3.connect(self.database_path, check_same_thread=False)

    @classmethod
    def initialize(self) -> None:
        home_path = os.path.expanduser('~')
        sql_path = f'{home_path}/{conf.sql_folder}'
        os.makedirs(sql_path, exist_ok=True)
        database_path = f'{sql_path}/database.db'
        with open(database_path, 'w') as f:
            f.write('')
            pass
        
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        with open(f'initial.sql', 'r') as sql_script:
            cursor.executescript(sql_script.read())
        cursor.connection.commit()
        cursor.close()

    # 插入教師
    def insert_teacher(self, teacher: teacher) -> None:
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO teacher (name) VALUES (?)', (teacher.name,))
        cursor.connection.commit()
        cursor.close()