from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoAlertPresentException
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

    def __eliminate_alert(self):
        try:
            WebDriverWait(self.driver, 1).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
            self.driver.switch_to.default_content()
        except TimeoutException:
            pass
        except NoAlertPresentException:
            pass

    def __has_class_selection(self):
        WebDriverWait(self.driver, 10).until((EC.presence_of_element_located((By.ID, self.degree_selection_id))))
        try:
            self.driver.find_element(By.ID, self.class_selection_id)
            return True
        except:
            return False

    # 取得學制選項
    def __get_degree_selection(self):
        degree_selection_element = WebDriverWait(self.driver, 10).until((EC.presence_of_element_located((By.ID, self.degree_selection_id))))
        self.degree_selection = Select(degree_selection_element)

    # 取得系所選項
    def __get_department_selection(self):
        department_selection_element = WebDriverWait(self.driver, 10).until((EC.presence_of_element_located((By.ID, self.department_selection_id))))
        self.department_selection = Select(department_selection_element)

    # 取得班級選項
    def __get_class_selection(self):
        assert(self.__has_class_selection())
        class_selection_element = WebDriverWait(self.driver, 10).until((EC.presence_of_element_located((By.ID, self.class_selection_id))))
        self.class_selection = Select(class_selection_element)
    
    # 取得查詢按鈕
    def __get_query_button(self):   
        WebDriverWait(self.driver, 10).until((EC.presence_of_element_located((By.ID, self.degree_selection_id))))
        self.query_button = self.driver.find_element(By.ID, self.query_button_id)
    
    # 選擇下一個學制
    def select_next_degree(self):
        self.__get_degree_selection()
        self.degree_selection.select_by_index(self.degree_selection_counter)
        self.degree_selection_counter += 1
        
    # 選擇下一個系所
    def select_next_department(self):
        self.__get_department_selection()
        self.department_selection.select_by_index(self.department_selection_counter)
        self.department_selection_counter += 1

    # 選擇下一個班級
    def select_next_class(self):
        # 班級選擇
        self.__get_class_selection()
        self.class_selection.select_by_index(self.class_selection_counter)
        self.class_selection_counter += 1

    # 取得班級名稱
    def get_class_name(self) -> str:
        self.__get_class_selection()
        return self.class_selection.first_selected_option.text       

    # 是否有下一個選項

    def has_next_degree(self) -> bool:
        self.__get_degree_selection()
        return self.degree_selection_counter < len(self.degree_selection.options)

    def has_next_department(self) -> int:
        self.__get_department_selection()
        return self.department_selection_counter < len(self.department_selection.options)

    def has_next_class(self) -> int:
        if (not self.__has_class_selection()):
            return False
        self.__get_class_selection()
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
        self.__get_query_button()
        self.driver.execute_script("arguments[0].click();", self.query_button)
        self.__eliminate_alert()