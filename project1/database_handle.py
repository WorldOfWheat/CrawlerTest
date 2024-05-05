from bs4 import BeautifulSoup
from site_data import *
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configuration
import threading
import requests

url = configuration.url
headers = configuration.headers

class question_handler():
    def __init__(self, 
                link: str
            ):
        self.link = link
    
    def __remove_html_tag(self, text: str) -> str:
        return BeautifulSoup(text, 'html5lib').text
    
    def __get_question(self, source) -> str:
        soup = BeautifulSoup(source, 'html5lib')
        question_date = soup.find('p', class_='date')
        question_div = question_date.find_parent().find(text=True, recursive=False)
        question = question_div.text.strip()
        return question
    
    def __get_answer(self, source) -> str:
        soup = BeautifulSoup(source, 'html5lib')
        thanks_button = soup.find('button', string='我要感謝')
        answer_div = thanks_button.findParent().find('textarea')
        answer = answer_div.text.strip().replace('<br>', '').replace('<br/>', '')
        return answer
    
    def get_q_and_a(self) -> q_and_a:
        source = requests.get(f'{url}{self.link}').text
        question = self.__get_question(source)
        answer = self.__get_answer(source)
        print(f'Question: {question}')
        print(f'Answer: {answer}')
        new_q_and_a = q_and_a(question, answer)
        return new_q_and_a

class database_handler():
    def __init__(self, 
                driver: webdriver
            ):
        self.driver = driver

    def __page_load_finish_check(self) -> None:
        # 等待「登入/註冊」按鈕出現
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'i.fas.fa-user.hidden-xs.hidden-sm')))

    # 判斷是否有下一頁
    def __has_next_page(self, source) -> bool:
        soup = BeautifulSoup(source, 'html5lib')
        next_symbol = soup.find('i', class_=['fa', 'fa-angle-right'])
        next_a_element = next_symbol.find_parent()
        return next_a_element.has_attr('id')
    
    # 前往下一頁
    def __goto_next_page(self) -> bool:
        # 按下一頁
        next_a_element = self.driver.find_element(By.ID, 'page-next')
        next_a_element.click()
        # 等待頁面載入完成
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.invisibility_of_element((By.ID, "loading")))
        return True

    # 判斷是否為 question a
    def __question_a_filter(self, a: str) -> bool:
        if not a.has_attr('href'):
            return False

        href = a['href']
        if href.find('single?') == -1:
            return False
        if href.find('inquiryId') == -1:
            return False
        if href.find('accessKey') == -1:
            return False
        return True   

    # 取得所有的 question a element
    def __get_all_question_a(self, source):
        soup = BeautifulSoup(source, 'html5lib')
        a_elements = soup.find_all('a')
        filtered_a_elements = []       
        for a in a_elements:
            if (not self.__question_a_filter(a)):
                continue
            filtered_a_elements.append(a)
        return filtered_a_elements

    # 將 a element 轉換成 link
    def __convert_question_a_to_link(self, a_elements):
        question_links = []
        for a in a_elements:
            question_links.append(a['href'])
        return question_links

    # 取得所有 Q&A
    def get_q_and_a(self, 
                   handle_section: section,
                   lock: threading.Lock = threading.Lock(),
                   semaphore: threading.Semaphore = threading.Semaphore(1)
                ) -> None:

        self.driver.get(f'{url}{handle_section.database_link}')       
        self.__page_load_finish_check()
        while True:
            source = self.driver.page_source
            # 取得所有的 question link
            a_elements = self.__get_all_question_a(source)
            # 將 question link 轉換成 link
            question_links = self.__convert_question_a_to_link(a_elements)
            # 取得所有的 Q&A
            for question_link in question_links:
                # 取得 Q&A
                q_and_a = question_handler(question_link).get_q_and_a()

                # 寫入資料
                lock.acquire()
                handle_section.q_and_a_list.append(q_and_a)
                lock.release()

            if (not self.__has_next_page(source)):
                break
            self.__goto_next_page()
        
        self.driver.quit()
        semaphore.release()