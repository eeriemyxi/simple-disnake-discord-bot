import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get('https://disnake.readthedocs.io/en/latest/api.html').text, 'html.parser')

names = soup.find_all('dt', attrs = {'class':'sig sig-object py'})
names = [i['id'] for i in names]
print(names)