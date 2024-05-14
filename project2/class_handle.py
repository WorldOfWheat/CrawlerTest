from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from site_data import *
from time import sleep

class class_handler:
    def __init__(self, 
                driver: webdriver
            ) -> None:
        self.driver = driver
        self.class_table_id = 'ctl00_ContentPlaceHolder1_GridView1'  
    
    def __get_class_table_rows(self):
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        class_table = soup.find('table', id=self.class_table_id)
        rows = class_table.find_all('tr')
        return rows
    
    def __get_teacher_name(self, row) -> list[teacher]:
        cells = row.find_all('td')
        teacher_name = cells[4].text
        teacher_name = teacher_name.replace('\n', '')

        if (len(teacher_name) <= 1 or teacher_name == '未定'):
            return []

        if (teacher_name.find(',') != -1):
            teacher_names = teacher_name.split(',')
            teacher_objects = []
            for name in teacher_names:
                new_teacher = teacher(name)
                teacher_objects.append(new_teacher)
            return teacher_objects
        
        new_teacher = teacher(teacher_name)
        return [new_teacher]

    # 是否為多頁
    def __is_multi_page(self, row) -> bool:
        cells = row.find_all('td')
        return cells[0].text == '1'
    
    # 前往下一頁
    def __goto_next_page(self, next_page_number):
        next_page_a_element = self.driver.find_element(By.XPATH, f'//a[text()="{next_page_number}"]')
        self.driver.execute_script("arguments[0].click();", next_page_a_element)
    
    # 是否有下一頁
    def __has_next_page(self, page_select_row, next_page_number) -> bool:
        page_select_span = page_select_row.find('a', text=f'{next_page_number}')
        if (page_select_span == None):
            return False
        return True
    
    # 是否有課程表
    def has_class_table(self):
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        no_data_td = soup.find('td', text='查無資料，請重新搜尋！')
        return no_data_td == None
    
    def get_teachers(self) -> list[str]:
        if (not self.has_class_table()):
            return []

        rows = self.__get_class_table_rows()
        # 移除表頭
        rows.remove(rows[0])

        teachers = []

        if (self.__is_multi_page(rows[-1])):
            next_page_number = 2
            while True:
                for row in rows[0:-2]:
                    teachers.extend(self.__get_teacher_name(row))
                
                page_select_row = rows[-1]

                # 沒有下一頁
                if (not self.__has_next_page(page_select_row, next_page_number)):
                    break

                self.__goto_next_page(next_page_number)
                next_page_number += 1
                rows = self.__get_class_table_rows()
                rows.remove(rows[0])
            print(list(map(str, teachers)))
            return teachers

        for row in rows:
            teachers.extend(self.__get_teacher_name(row))

        return teachers
