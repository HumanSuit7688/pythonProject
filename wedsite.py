from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

# agent =  {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
url = 'https://stopgame.ru/news'

ua = UserAgent()
headers = {'User-Agent': ua.random}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
quest = soup.find_all('div', class_ = 'item article-summary')

titles = []

for t in quest:
    tit = t.find('div', class_ = 'caption caption-bold').text
    titles.append(tit)

for a in titles:
    print(a)