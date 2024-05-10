from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class panel_handler:
    def __init__(self, 
                driver: webdriver
            ) -> None:
        self.driver = driver
        # 學制、系承、班級計數器歸零
        self.degree_selection_counter = 0
        self.department_selection_counter = 0
        self.class_selection_counter = 0
        # selections ID
        self.degree_selection_id = 'ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_ddl_class_edusys'
        self.department_selection_id = 'ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_ddl_class_dept'
        self.class_selection_id = 'ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_lbox_general'
        self.query_button_id = 'ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_btn_queryclass'

        self.__get_panel_elements()
    
    # 取得班級選項
    def __get_class_selection(self):
        self.class_selection = Select(self.driver.find_element(By.ID, self.class_selection_id))
    
    # 取得學制、系所選項、查詢按鈕
    def __get_panel_elements(self):
        self.degree_selection = Select(self.driver.find_element(By.ID, self.degree_selection_id))
        self.department_selection = Select(self.driver.find_element(By.ID, self.department_selection_id))
        self.query_button = self.driver.find_element(By.ID, self.query_button_id)
    
    # 選擇下一個學制
    def select_next_degree(self):
        self.degree_selection.select_by_index(self.degree_selection_counter)
        self.degree_selection_counter += 1
        
    # 選擇下一個系所
    def select_next_department(self):
        self.department_selection.select_by_index(self.department_selection_counter)
        self.department_selection_counter += 1

    # 選擇下一個班級
    def select_next_class(self):
        # 班級選擇
        self.class_selection.select_by_index(self.class_selection_counter)
        self.class_selection_counter += 1

    # 是否有下一個選項
    def has_next_degree(self) -> bool:
        return self.degree_selection_counter < len(self.degree_selection.options)

    def has_next_department(self) -> int:
        return self.department_selection_counter < len(self.department_selection.options)

    def has_next_class(self) -> int:
        return self.class_selection_counter < len(self.class_selection.options)
    
    # 計數器歸零
    def reset_degree_counter(self) -> None:
        self.degree_selection_counter = 0
    
    def reset_department_counter(self) -> None:
        self.department_selection_counter = 0
        
    def reset_class_counter(self) -> None:
        self.class_selection_counter = 0

    # 點擊查詢按鈕
    def click_query_button(self):
        self.query_button.click()
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.ID, self.query_button_id)))
        self.__get_panel_elements()
        self.__get_class_selection()
    
    def accept_pop_out(self):
        self.driver.switch_to.alert.accept()
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Label7')))
        self.__get_panel_elements()