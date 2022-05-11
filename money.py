from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent


url1 = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=RUB'
url2 = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=EUR&To=RUB'
ua = UserAgent()

headers = {'User-Agent': ua.random}
response = requests.get(url1, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
quest = soup.find('p', class_='result__BigRate-sc-1bsijpp-1 iGrAod')


Usd = quest.text
print("1 American Dollar = " + Usd)

# Eur = quest.text
# print("1 European Euro = " + Eur)