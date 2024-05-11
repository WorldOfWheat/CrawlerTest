from bs4 import BeautifulSoup
from site_data import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sql_handle import sql_handler
import configuration
import re
import threading

url = configuration.url

class department_handler:
    def __init__(self, driver: webdriver):
        self.driver = driver
        self.sql = sql_handler()

    # 等待網頁載入完成
    def __page_load_finish_check(self):        
        # 等待「登入/註冊」按鈕出現
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'i.fas.fa-user.hidden-xs.hidden-sm')))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.wrapper')))

    # 取得所有的 department
    # 使用前請確保已經進入科別總覽
    def __get_all_departments(self) -> list[department]:
        # 確定已經進入科別總覽
        assert self.driver.current_url.find('department_all') != -1

        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html5lib')

        departments = []
        # 取得 department tab
        department_tab = soup.find('ul', id='division-tab-list')
        for a in department_tab.find_all('a'):
            # 將 id 取出
            department_id = re.sub('.*-.*-', '', a['id'])

            new_department = department(id=department_id, print_name=a.text)
            departments.append(new_department)
        
        return [department(id='SUG', print_name='內科')]
        return departments

    # 取得所有的 section
    # 使用前請確保已經進入科別總覽
    def __get_all_sections(self, handle_deparment : department):
        # 確定已經進入科別總覽
        assert self.driver.current_url.find('department_all') != -1
        
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html5lib')
        # 取得 section list
        sections_tbody = soup.find('tbody', id=f'section-list-{handle_deparment.id}')
        # 取得所有 section 的 a
        a_elements =  sections_tbody.find_all('a')
        handle_deparment.sections = []
        for a in a_elements:
            # 取得 section_id
            section_id = a.find_parent('tr')['id']
            new_section = section(id=section_id, link=a['href'], print_name=a.text)
            handle_deparment.sections.append(new_section)

    # 取得進入科別總覽的 script
    def get_department_list_enter_script(self) -> str:
        # 檢查是否已經進入網頁
        if (self.driver.current_url.find('kingnet.com.tw') == -1):
            raise Exception('Please enter site first')

        self.__page_load_finish_check()

        # 取得網頁原始碼
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html5lib')

        # 找到 “我要諮詢” 按鈕，之後找到下一個 li    
        start_menu_options = soup.find('li', string='我要諮詢').findNextSibling()
        a = start_menu_options.findNext()
        onclick_script = a['onclick']

        return onclick_script


    # 取得所有 department 和其 section 的連結
    def get_all_departments_and_sections(self) -> list[department]:
        # 檢查是否已經進入科別總覽
        if (self.driver.current_url.find('department_all') == -1):
            raise Exception('Please enter department list first')

        try:
            # 等待網頁載入完成
            self.__page_load_finish_check()
        
            # 取得所有 department
            departments = self.__get_all_departments()
            departments.pop() 

            # 取得所有 section
            for department in departments:
                self.__get_all_sections(department)

            # 寫入資料庫
            for department in departments:
                self.sql.add_department(department)
                for section in department.sections:
                    self.sql.add_section(department, section)
            
            return departments
        
        except Exception as e:
            raise Exception(f'Getting all departments and sections Error\n{e}')

    # 取得所有的 database link
    def get_all_sections_database_link(self, 
                                       handle_department: department, 
                                       lock: threading.Lock = threading.Lock(),
                                       semaphore: threading.Semaphore = threading.Semaphore(1)
                                    ) -> None:
        try:
            for section in handle_department.sections:
                try:
                    self.driver.get(f'{url}{section.link}')
                    self.__page_load_finish_check()

                    # 取得網頁原始碼
                    web_source = self.driver.page_source
                    soup = BeautifulSoup(web_source, 'html5lib')

                    # 找到第一顆「更多」的 a
                    more_a_element = soup.find('a',id='more-section-inquiry-href')

                    # 如果沒有 href，重新載入
                    if (not more_a_element.has_attr('href')):
                        self.driver.execute_script(f'location.reload()')
                        self.__page_load_finish_check()
                        web_source = self.driver.page_source
                        soup = BeautifulSoup(web_source, 'html5lib')
                        more_a_element = soup.find('a',id='more-section-inquiry-href')

                    # 寫入資料 
                    with lock:
                        section.database_link = more_a_element['href']
                except Exception as e:
                    raise Exception(f'\t{section.id}\n{e}')

        except Exception as e:
            print(f'Getting database links error')
            print(f'\t{handle_department.id}')
            print(f'{e}')

        finally:
            self.driver.quit()
            semaphore.release()