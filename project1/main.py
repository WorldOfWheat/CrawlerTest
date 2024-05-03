from bs4 import BeautifulSoup
from databases_handle import databases_handler
from department_handle import department_handler
from time import sleep
import instances
import temp_handle as temp_handle
import os
import requests

url = instances.url
headers = instances.headers
file_names = instances.file_names
driver = instances.driver

# 結束時的動作
def end():
    # 結束時將清空暫存檔，並刪除暫存檔
    for key in file_names:
        temp_handle.write(file_names[key], '')
        os.remove(f'{temp_handle.temp_folder}/{file_names[key]}')
    driver.quit()

def section_a_filter(href: str) -> bool:
    return href.find('sectionId') != -1

# 取得下一個 common 的 index
def next_common(string, current_index) -> str:
    return string.find(',', current_index) + 1

# 取得內科的進入 script
def get_first_subject_script() -> str:
    web = requests.get(url, headers=headers)
    web.encoding = 'utf8'

    soup = BeautifulSoup(web.text, 'html5lib')
    # 找到 “我要諮詢” 按鈕，之後找到下一個 li    
    start_menu_options = soup.find('li', string='我要諮詢').findNextSibling()
    a = start_menu_options.findNext()
    onclick_script = a['onclick']
    return onclick_script

# 取得所有的 section 的 url
# 使用前請先確保已經進入內科
def get_sorted_department_section_urls() -> dict[str, list[dict[str, str]]]:
    # 對 section_1_source 進行解析
    source = temp_handle.read(file_names['section_1_source'])
    soup = BeautifulSoup(source, 'html5lib')
    # 找到所有的超連結
    a_elements = soup.find_all('a')
    # 過濾出所有的 section 的 a
    filtered_a_elements = []
    for a in a_elements:
        if not a.has_attr('href'):
            continue
        if (not section_a_filter(a['href'])):
            continue
        filtered_a_elements.append(a)
    filtered_a_elements = filtered_a_elements[0:-2]  # 最後兩個是不需要的 []

    # 分類
    sorted_a_elements = {}
    department_counter = 0
    for a in filtered_a_elements:
        # 按 tbody id 分類 aka 部門 id
        tbody = a.find_parent('tbody')
        department_id = tbody['id']

        if department_id not in sorted_a_elements:
            sorted_a_elements[department_id] = []
            department_counter = 0

        sorted_a_elements[department_id].append({'href': a['href'], 'id': department_counter})
        department_counter += 1

    return sorted_a_elements

def main():
    # 進入網站
    driver.get(url)

    # 找到進入所有科別的 script，並執行
    first_subject_script = get_first_subject_script()
    driver.execute_script(first_subject_script)
    sleep(0.5)

    # 取得所有科別的網頁原始碼
    web_source = driver.page_source
    temp_handle.write(file_names['section_1_source'], web_source)
    sleep(0.1)

    # 取得所有科別的 url
    department_section_urls = get_sorted_department_section_urls()
    department_section_database_links = {}
    for department_id in department_section_urls:
        department_handle = department_handler(department_section_urls[department_id])
        department_section_database_links[department_id] = department_handle.get_all_database_link()
        break # TODO

    # 得科別 database link 得到 question link
    print(department_section_database_links)
    question_links = {}
    for department_id in department_section_urls:
        print(department_id)
        question_links[department_id] = {}
        for i in range(len(department_section_database_links[department_id])):
            question_links[department_id][i] = databases_handler(department_section_database_links[department_id][i])
        break # TODO

if __name__ == '__main__':
    print('test2.py is running...')
    main()
    end()