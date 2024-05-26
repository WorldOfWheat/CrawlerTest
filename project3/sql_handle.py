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
    def add_page(self, 
                added_page: page
            ) -> None:
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO page (page_number, content) VALUES (?,?)', (added_page.page_number, added_page.content))
        cursor.connection.commit()
        cursor.close()
    
    def __get_all_pages(self) -> list[page]:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM page')
        pages = cursor.fetchall()
        cursor.close()
        return pages

    
    def to_file(self,
                directory_path: str
            ):
        directory_path = os.path.expanduser(directory_path)
        os.makedirs(directory_path, exist_ok=True)
        pages = self.__get_all_pages()
        html_template_code = '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>#</body></html>'
        for page in pages:
            with open(f'{directory_path}/{page[0]}.html', 'w') as f:
                html_code = html_template_code.replace('#', page[1])
                f.write(html_code)
