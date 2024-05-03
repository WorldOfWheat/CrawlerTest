from random import randbytes
from selenium import webdriver

url = 'https://www.kingnet.com.tw'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

file_names : dict[str, str] = {
    'section_1_source': randbytes(32).hex(),
}

opt = webdriver.ChromeOptions()
opt = opt.add_argument(f'--user-agent={headers["user-agent"]}')
driver = webdriver.Chrome(options=opt)