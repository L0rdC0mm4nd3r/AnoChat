#!/usr/bin/python3
from urllib.request import urlopen
from bs4 import BeautifulSoup

#---------------Check if there is a new version---------------#
#-------------------------------------------------------------#
def check_update():
	response = urlopen('https://github.com/L0rdC0mm4nd3r/AnoChat/blob/master/server/config/version.txt')
	soup = BeautifulSoup(response, 'html.parser')
	contents = soup.find_all('td')

	git_version = []
	version = '0.1'
	changes = ''

	for content in contents:
		content = str(content.string).strip()
		if content != 'None':
			git_version.append(content)
			changes += content+'\n'

	if version != git_version[0]:
		print('[?] Update available\n')
		print('\033[1mVersion:\033[m',git_version[0])		
		print('\033[1mCHANGES\033[m')
		print(changes)

