from bs4 import BeautifulSoup
import instances

url = instances.url
headers = instances.headers
driver = instances.driver

class database_handler(threading.Thread):
    def __init__(self, driver, database_link, department_id, result):
        # 變數 initial
        self.databases_urls = databases_urls
        self.question_links = []
    
    def _has_next_page(self, source) -> bool:
        soup = BeautifulSoup(source, 'html5lib')
        next_a_element = soup.find('a', id='page-next')
        if next_a_element is None:
            return False
        return True
    
    def _question_href_filter(self, href: str) -> bool:
        if href.find('single?') == -1:
            return False
        if href.find('inquiryId') == -1:
            return False
        if href.find('accessKey') == -1:
            return False
        return True   
    
    def _get_all_question_a(self, source):
        soup = BeautifulSoup(source, 'html5lib')
        a_elements = soup.find_all('a')
        filtered_a_elements = []       
        for a in a_elements:
            if not a.has_attr('href'):
                continue
            if (not self._question_href_filter(a['href'])):
                continue
            filtered_a_elements.append(a)

    
    # def run(self) -> None:
    def run(self) -> None:
        print(f'{url}{self.database_link}')
        self.driver.get(f'{url}{self.database_link}')
        while True:
            sleep(2)
            source = self.driver.page_source 

            # 取得所有的 question link

            # 取得網頁原始碼
            web_source = driver.page_source
            self.question_links.append(self._get_all_question_a(web_source))
            
        print(self.question_links)
        return self.question_links       