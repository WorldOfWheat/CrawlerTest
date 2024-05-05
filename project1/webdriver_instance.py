from selenium import webdriver
import project1.configuration as configuration

headers = configuration.headers

opt = webdriver.ChromeOptions()
opt = opt.add_argument(f'--user-agent={headers["user-agent"]}')
driver = webdriver.Chrome(options=opt)