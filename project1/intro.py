from bs4 import BeautifulSoup
import defination
import requests

url = defination.url
headers = defination.headers

# 取得下一個 common 的 index
def next_common(string, current_index) -> str:
    return string.find(',', current_index) + 1

# 取得內科的進入 script
def get_first_department_enter_script() -> str:
    web = requests.get(url, headers=headers)
    web.encoding = 'utf8'

    soup = BeautifulSoup(web.text, 'html5lib')
    # 找到 “我要諮詢” 按鈕，之後找到下一個 li    
    start_menu_options = soup.find('li', string='我要諮詢').findNextSibling()
    a = start_menu_options.findNext()
    onclick_script = a['onclick']

    return onclick_script