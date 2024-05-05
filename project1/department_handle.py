from bs4 import BeautifulSoup
from site_data import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configuration
import threading

url = configuration.url

class department_handler:
    def __init__(self, driver: webdriver):
        self.driver = driver

    # 等待網頁載入完成
    def __page_load_finish_check(self):        
        # 等待「登入/註冊」按鈕出現
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'i.fas.fa-user.hidden-xs.hidden-sm')))

    # 檢查 a 是否為 section
    def __section_a_filter(self, a: str) -> bool:
        if not a.has_attr('href'):
            return False
        return a['href'].find('department?sectionId') != -1

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

    # 取得所有 department 的連結
    def get_all_department(self) -> list[department]:
        # 檢查是否已經進入科別總覽
        if (self.driver.current_url.find('department_all') == -1):
            raise Exception('Please enter department list first')

        self.__page_load_finish_check()
        
        # 對科別總覽進行解析
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html5lib')

        # 對每個 section 做分類
        department_sections = {}

        # 找到所有的超連結
        a_elements = soup.find_all('a')
        filtered_a_elements = []
        for a in a_elements:
            # 過濾出所有的 section 的 a
            if (not self.__section_a_filter(a)):
                continue
            filtered_a_elements.append(a)

            # 將 section 加入 department_sections
            department_name = a.find_parent('tbody')['id']

            # 過濾掉 search-section-list
            if (department_name == 'search-section-list'):
                continue

            # 將 section 加入 department_sections
            if (department_name not in department_sections):
                department_sections[department_name] = []
            department_sections[department_name].append(section(link=a['href'], print_name=a.text))

            break #TODO

        # 對每個 section 做分類
        department_list = []
        for department_name in department_sections.keys():
            department_list.append(department(name=department_name, sections=department_sections[department_name]))

        return department_list
        

    # 取得所有的 database link
    def get_all_sections_database_link(self, 
                                       handle_department: department, 
                                       lock: threading.Lock = threading.Lock(),
                                       semaphore: threading.Semaphore = threading.Semaphore(1)
                                    ) -> None:

        for section in handle_department.sections:
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
            lock.acquire()
            section.database_link = more_a_element['href']
            lock.release()

        self.driver.quit()
        semaphore.release()