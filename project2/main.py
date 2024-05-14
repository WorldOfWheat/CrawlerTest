from class_handle import class_handler
from panel_handle import panel_handler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from sql_handle import sql_handler
from time import sleep
import configuration as conf
import threading

url = conf.url
headers = conf.headers

# 等待所有執行緒結束
def wait_threads(threads: list[threading.Thread]):
    for thread in threads:
        thread.join()

# 取得新的 webdriver
def get_new_webdriver(added_options) -> webdriver:
    options = webdriver.ChromeOptions()
    options.binary_location = 'chrome-linux64/chrome'
    for added_option in added_options:
        options.add_argument(added_option)
    
    service = Service('chromedriver-linux64/chromedriver')
    new_driver = webdriver.Chrome(service=service, options=options)

    return new_driver

driver = get_new_webdriver([headers['user-agent']])

def main():
    # 初始化 SQL 資料庫
    sql_handler.initialize()   

    # 進入網站
    driver.get(url)

    class_handle = class_handler(driver)
    panel_handle = panel_handler(driver)
    panel_handle.select_next_degree()
    panel_handle.select_next_department()
    while (panel_handle.has_next_degree()):
        panel_handle.select_next_degree()
        while (panel_handle.has_next_department()):
            try:
                panel_handle.select_next_department()
                panel_handle.click_query_button()
                while (panel_handle.has_next_class()):
                    panel_handle.select_next_class()
                    class_handle.get_teachers()
                panel_handle.reset_class_counter()
            except Exception as e:
                print(f'\t{panel_handle.get_class_name()}')
                print(e)
        panel_handle.reset_department_counter()

    driver.quit()
    sleep(5)


if __name__ == '__main__':
    main()