from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from site_data import *

class subject_handler():
    def __init__(self,
                driver: webdriver
            ) -> None:
            self.__driver = driver
            self.__element_id = {
                'id': 'ctl00_ContentPlaceHolder1_CourseDetail_onepage1_lab_subcode',
                'subject_name': 'ctl00_ContentPlaceHolder1_CourseDetail_onepage1_lab_subname_ch',
                'subject_eng_name': 'ctl00_ContentPlaceHolder1_CourseDetail_onepage1_lab_subname_en',
                'credit': 'ctl00_ContentPlaceHolder1_CourseDetail_onepage1_lab_credit',
                'teacher_info_table': 'ctl00_ContentPlaceHolder1_CourseDetail_onepage1_GridView1',
                'required': 'ctl00_ContentPlaceHolder1_CourseDetail_onepage1_lab_rs',
                'time_and_room_table': 'ctl00_ContentPlaceHolder1_CourseDetail_onepage1_lab_room'
            }
            self.__weekday = {
                '週一': 1,
                '週二': 2,
                '週三': 3,
                '週四': 4,
                '週五': 5,
                '週六': 6,
                '週日': 7
            }
    
    def __get_id(self) -> str:
        return self.__driver.find_element(By.ID, self.__element_id['id']).text
    
    def __get_subject_name(self) -> str:
        return self.__driver.find_element(By.ID, self.__element_id['subject_name']).text
    
    # 取得英文名稱
    def __get_subject_eng_name(self) -> str:
        return self.__driver.find_element(By.ID, self.__element_id['subject_eng_name']).text
    
    # 取得學分
    def __get_credit(self) -> int:
        return int(self.__driver.find_element(By.ID, self.__element_id['credit']).text)
    
    # 取得教師
    def __get_teacher(self) -> teacher:
        teacher_info_table = self.__driver.find_element(By.ID, self.__element_id['teacher_info_table'])
        teacher_name = teacher_info_table.find_element(By.TAG_NAME, 'td').text
        return teacher(teacher_name)
    
    # 取得是否為必修
    def __get_required(self) -> bool:
        return self.__driver.find_element(By.ID, self.__element_id['required']).text.find('必修') != -1
    
    # 從字串中取得第一個數字
    def __get_number(self, text: str) -> int:
        number_counter = 0
        for character in text:
            if (character.isdigit()):
                break
            number_counter += 1

        number = 0
        for character in text[number_counter:]:
            if (not character.isdigit()):
                break
            number = number * 10 + int(character)
    
    # 取得時間
    def __get_time(self) -> list[subject_time]:
        time_and_room_table = self.__driver.find_element(By.ID, self.__element_id['time_and_room_table'])
        span_text = time_and_room_table.text
        time_and_room_texts = span_text.split('<br>')

        new_subject_times = []
        day = time_and_room_text[1:3]
        new_subject_time.set_day(self.__weekday[day])
        for time_and_room_text in time_and_room_texts:
            new_subject_time = subject_time()
            # 設定星期
            day = self.__weekday[time_and_room_text[1:3]]
            new_subject_time.set_day(day)
            # 設定節次
            section = self.__get_number(time_and_room_text)
            new_subject_time.add_section(section)
    
    def get_subject(self) -> subject:
        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.ID, self.__element_id['id'])))

        new_subject = subject(
            id = self.__get_id(),
            subject_name = self.__get_subject_name(),
            subject_eng_name = self.__get_subject_eng_name()
        )
        