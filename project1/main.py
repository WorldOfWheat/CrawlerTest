from database_handle import database_handler
from department_handle import department_handler
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sql_handle import sql_handler
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
    sql_handler().initialize()   

    # 進入網站
    driver.get(url)

    department_handle = department_handler(driver)
    # 找到進入所有科別的 script，並執行
    department_list_enter_script = department_handle.get_department_list_enter_script()
    driver.execute_script(department_list_enter_script)

    # 等待科別總覽載入完成
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains('department_all'))

    print("Getting all departments data")
    all_departments = department_handle.get_all_departments_and_sections()

    # 取得所有 department 的 section 的 database link
    semaphore = threading.Semaphore(3)
    lock = threading.Lock()
    threads = []
    for department in all_departments:
        semaphore.acquire()
        new_driver = get_new_webdriver([headers['user-agent']])
        print(f'Getting {department.name} database links')
        thread = threading.Thread(target=department_handler(new_driver).get_all_sections_database_link, args=(department, lock, semaphore))
        thread.start()
        threads.append(thread)

    # 等待所有 thread 結束
    wait_threads(threads)
    
    # 取得所有 department 的 section 的 Q&A
    semaphore = threading.Semaphore(3)
    for department in all_departments:
        for section in department.sections:
            print(f'Getting {department.name} - {section.id} Q&A')
            semaphore.acquire()
            new_driver = get_new_webdriver([headers['user-agent'], 'window-size=1400,900'])
            thread = threading.Thread(target=database_handler(new_driver).get_q_and_a, args=(section, lock, semaphore))
            thread.start()
            threads.append(thread)

    # 等待所有 thread 結束
    wait_threads(threads)

if __name__ == '__main__':
    main()