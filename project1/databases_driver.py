from databases_handle import database_handler
from selenium import webdriver
import threading
import instances
import time

headers = instances.headers

def get_new_driver() -> webdriver.Chrome:
    opt = webdriver.ChromeOptions()
    opt = opt.add_argument(f'--user-agent={headers["user-agent"]}')
    new_driver = webdriver.Chrome(options=opt)
    return new_driver

def get_all_department_question_links(department_section_database_links : dict[str, list]) -> dict[str, list]:
    department_section_questions = {}
    threads = []
    for department_id in department_section_database_links.keys():
        print(len(department_section_database_links[department_id]))
        for i in range(len(department_section_database_links[department_id])):
            print(f'Processing {department_id} {i}...')
            threads.append(database_handler(get_new_driver(), department_section_database_links[department_id][i], department_id, department_section_questions))
            threads[-1].start()
    
    for thread in threads:
        thread.join()
    
    return department_section_questions