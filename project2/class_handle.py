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

    def __is_multi_page(self, row) -> bool:
        cells = row.find_all('td')
        return cells[0].text == '1'
    
    def __goto_next_page(self, page_select_row):
        # TODO
        next_page_a = page_select_row.find('span').find_parent('td').find_next_sibling().find('a')
        next_page_a_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//a[@href ='{next_page_a['href']}']")))
        self.driver.execute_script("arguments[0].click();", next_page_a_element)
    
    def __has_next_page(self, page_select_row) -> bool:
        next_page_a = page_select_row.find('span').find_parent('td').find_next_sibling().find('a')
        return next_page_a != None
    
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
            while True:
                for row in rows[0:-2]:
                    teachers.extend(self.__get_teacher_name(row))
                print(list(map(str, teachers)))
                
                page_select_row = rows[-1]

                # 沒有下一頁
                print(page_select_row)
                if (not self.__has_next_page(page_select_row)):
                    break
                print(page_select_row)

                print('next page')
                self.__goto_next_page(page_select_row)
                sleep(10)
                rows = self.__get_class_table_rows()
                rows.remove(rows[0])
            return teachers

        for row in rows:
            teachers.extend(self.__get_teacher_name(row))

        return teachers
