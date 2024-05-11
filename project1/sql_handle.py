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
    
    # 增加 department
    def add_department(self, 
                       added_department: department
                    ) -> None:
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO departments (department_id, print_name) VALUES (?,?)', (added_department.id, added_department.print_name))
        cursor.connection.commit()
        cursor.close()
    
    # 增加 section
    def add_section(self, 
                   added_section_department: department,
                   added_section: section,
                ) -> None:
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO sections (section_id, print_name, department_id) VALUES (?,?,?)', 
                       (added_section.id, added_section.print_name, added_section_department.id))
        cursor.connection.commit()
        cursor.close()
    
    # 增加新的 Q&A
    def add_q_and_a(self,
                     added_q_and_a_section: section,
                     added_q_and_a: q_and_a
                 ) -> None:
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO q_and_a_pairs (question,answer,section_id) VALUES (?, ?, ?)', 
                       (added_q_and_a.question, added_q_and_a.answer, added_q_and_a_section.id))
        cursor.connection.commit()
        cursor.close()
    
