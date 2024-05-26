from bs4 import BeautifulSoup
from site_data import *
import configuration as conf
import requests
import threading

class handler:
	def __init__(self,
		 		index: int,
	  			href: str,
			):
		self.index = index
		self.href = href
	
	def get_content(self,
                   request_semaphore: threading.Semaphore,
				   sql_lock: threading.Lock
				):
		with request_semaphore:
			request = requests.get(f'{conf.url}{self.href}', headers=conf.headers)
			request.encoding = 'utf-8'
			source = request.text
		soup = BeautifulSoup(source, 'html5lib')
		content = str(soup.find('div', id='nr1'))
		# 存入 SQL
		with sql_lock:
			page(self.index, content).save_to_sql()
