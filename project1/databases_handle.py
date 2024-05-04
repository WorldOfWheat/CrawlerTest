from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import threading
import instances

url = instances.url
headers = instances.headers

class database_handler(threading.Thread):
    def __init__(self, 
                database_link : str, 
                department_id : str, 
                result : dict[str, list],
                result_lock : threading.Lock,
                semaphore : threading.Semaphore
        ):
        threading.Thread.__init__(self)
        # 變數 initial
        self.database_link = database_link
        self.department_id = department_id
        self.question_links = result
        self.question_links_lock = result_lock
        self.semaphore = semaphore

    # 取得新的 driver
    def _get_new_driver(self) -> webdriver.Chrome:
        opt = webdriver.ChromeOptions()
        opt.add_argument(f'--user-agent={headers["user-agent"]}')
        opt.add_argument("--window-size=1400,900")
        new_driver = webdriver.Chrome(options=opt)
        return new_driver
    
    # 判斷是否有下一頁
    def _has_next_page(self, source) -> bool:
        soup = BeautifulSoup(source, 'html5lib')
        next_symbol = soup.find('i', class_=['fa', 'fa-angle-right'])
        next_a_element = next_symbol.find_parent()
        return next_a_element.has_attr('id')
    
    # 判斷是否為 question link
    def _question_href_filter(self, href: str) -> bool:
        if href.find('single?') == -1:
            return False
        if href.find('inquiryId') == -1:
            return False
        if href.find('accessKey') == -1:
            return False
        return True   
    
    # 取得所有的 question a element
    def _get_all_question_a(self, source):
        soup = BeautifulSoup(source, 'html5lib')
        a_elements = soup.find_all('a')
        filtered_a_elements = []       
        for a in a_elements:
            if not a.has_attr('href'):
                continue
            if (not self._question_href_filter(a['href'])):
                continue
            filtered_a_elements.append(a)
        return filtered_a_elements
    
    # 將 a element 轉換成 link
    def _convert_question_a_to_link(self, a_elements):
        question_links = []
        for a in a_elements:
            question_links.append(a['href'])
        return question_links
    
    def run(self) -> None:
        with self.semaphore:
            print(f'{url}{self.database_link}')
            driver = self._get_new_driver()
            driver.get(f'{url}{self.database_link}')
            while True:
                try:
                    wait = WebDriverWait(driver, 10)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'i.fa.fa-angle-right')))
                except TimeoutException:
                    print(self.department_id + ' TimeoutException')
                    break

                source = driver.page_source 

                # 取得所有的 question link
                a_elements = self._get_all_question_a(source)
                links = self._convert_question_a_to_link(a_elements)

                # 將 question link 加入 result
                self.question_links_lock.acquire()
                if (self.question_links.get(self.department_id) is None):
                    self.question_links[self.department_id] = []
                self.question_links[self.department_id].append(links)
                self.question_links_lock.release()

                # 如果沒有下一頁，則 break
                if not self._has_next_page(source):
                    break
                
                # 按下一頁
                next_a_element = driver.find_element(By.ID, 'page-next')
                next_a_element.click()