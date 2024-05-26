from bs4 import BeautifulSoup
from site_data import *
import configuration
import requests

class handler:
	def __init__(self, 
				url: str,
			):
		self.url = url
	
	def get_entrances(self) -> list:
		source = requests.get(self.url, headers=configuration.headers).text
		soup = BeautifulSoup(source, 'html5lib')
		table_div = soup.find('div', class_='book-list clearfix')
		links = table_div.find_all('a')
		entrances = []
		for page_number, link in enumerate(links, start=1):
			entrances.append(entrance(page_number, link['href']))
		return entrances
