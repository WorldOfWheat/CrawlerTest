from project1.database_handle import database_handler
from selenium import webdriver
import threading
import instances
import time

headers = instances.headers

def get_all_department_question_links(department_section_database_links : dict[str, list]) -> dict[str, list]:
    semaphore = threading.Semaphore(4)
    department_section_questions_lock = threading.Lock()
    department_section_questions = {}
    threads = []
    for department_id in department_section_database_links.keys():
        for i in range(len(department_section_database_links[department_id])):
            threads.append(database_handler(
                department_section_database_links[department_id][i], 
                department_id, 
                department_section_questions, 
                department_section_questions_lock,
                semaphore
            ))
            threads[-1].start()
    
    for thread in threads:
        thread.join()
    
    return department_section_questions