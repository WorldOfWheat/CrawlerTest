from panel_handle import panel_handler
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sql_handle import sql_handler
from time import sleep
import configuration as conf
import threading

url = conf.url
headers = conf.headers

def wait_threads(threads: list[threading.Thread]):
    for thread in threads:
        thread.join()

def get_new_webdriver(added_options) -> webdriver:
    options = webdriver.ChromeOptions()
    for added_option in added_options:
        options.add_argument(added_option)
    new_driver = webdriver.Chrome(options=options)
    return new_driver

driver = get_new_webdriver([headers['user-agent']])

def main():
    # 初始化 SQL 資料庫
    sql_handler.initialize()   

    # 進入網站
    driver.get(url)

    panel_handle = panel_handler(driver)
    panel_handle.select_next_degree()
    panel_handle.select_next_department()
    while (panel_handle.has_next_degree()):
        panel_handle.select_next_degree()
        while (panel_handle.has_next_department()):
            panel_handle.select_next_department()
            try:
                panel_handle.click_query_button()
            except UnexpectedAlertPresentException:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                sleep(10)
                panel_handle.accept_pop_out()
            except TimeoutException:
                continue
            except Exception as e:
                print(e)
            sleep(1)
        panel_handle.reset_department_counter()

    sleep(5)


if __name__ == '__main__':
    main()