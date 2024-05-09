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
    
    # 增加 section
    def add_section(self, 
                   added_section: section
                ) -> None:
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO sections (section_id) VALUES (?)', (added_section.id,))
        cursor.connection.commit()
        cursor.close()
    
    # 增加新的 Q&A
    def add_q_and_a(self,
                     q_and_a_section: section,
                     added_q_and_a: q_and_a
                 ) -> None:
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO q_and_a_pairs (section_id,question,answer) VALUES (?, ?, ?)', (q_and_a_section.id, added_q_and_a.question, added_q_and_a.answer))
        cursor.connection.commit()
        cursor.close()
    
    def debug_print(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM q_and_a_pairs')
        print(cursor.fetchall())
        cursor.connection.commit()
        cursor.close()
