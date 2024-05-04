from bs4 import BeautifulSoup
import instances

url = instances.url
headers = instances.headers
driver = instances.driver

class department_handler:
    def __init__(self, department_urls):
        # 變數 initial
        self.department_urls = department_urls
        self.database_links = []
    
    # 取得所有的 database link
    def get_all_database_link(self) -> None:
        for section_data in self.department_urls:
            # 取得網頁
            driver.get(f'{url}{section_data["href"]}')

            # 取得網頁原始碼
            web_source = driver.page_source
            soup = BeautifulSoup(web_source, 'html5lib')

            # 找到第一顆 “更多按鈕”
            more_a_button = soup.find('a', string='更多 >')
            self.database_links.append(more_a_button['href'])

        return self.database_links
        