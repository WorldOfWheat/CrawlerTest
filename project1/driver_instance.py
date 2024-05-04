from selenium import webdriver
import defination

headers = defination.headers

opt = webdriver.ChromeOptions()
opt = opt.add_argument(f'--user-agent={headers["user-agent"]}')
driver = webdriver.Chrome(options=opt)