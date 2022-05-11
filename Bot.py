import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import random
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands =['start'])
async def start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")

@dp.message_handler(commands = ['help'])
async def help_command(message: types.Message):
    await message.reply('gg')

# @dp.message_handler()
# async def words(message: types.Message):
#     kol = int(message.text.count(' ') + 1)
#     kol2 = int(len(message.text) + 1)
#     kol3 = kol2 - kol
#     await message.reply(str(kol) + " Слов\n"  + str(kol3) + " Букв")

button_game_news = KeyboardButton('/game_news')
greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_game_news)


@dp.message_handler(commands='News')
async def news_titles(message: types.Message):
    url = 'https://stopgame.ru/news'
    ua = UserAgent()

    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    quest = soup.find_all('div', class_='item article-summary')

    titles = []
    x = random.randint(0, 20)
    for t in quest:
        title = []
        titleName = t.find('div', class_='caption caption-bold').text
        titleLink = t.find('a')['href']
        title.append(titleName)
        title.append(titleLink)
        titles.append(title)
    text = titles[x][0] + '\n' + 'https://stopgame.ru' + titles[x][1]
    await message.reply(text)


inline_kb_usd = InlineKeyboardButton('Курс Доллара', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_kb_usd)
inline_kb_eur = InlineKeyboardButton('Курс Евро', callback_data='button2')
inline_kb2 = InlineKeyboardMarkup().add(inline_kb_eur)
inline_kb_full = InlineKeyboardMarkup(row_width=3).add(inline_kb_usd).add(inline_kb_eur)

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    Usd = take_money(url1)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"1 American Dollar = " + Usd)

@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    Eur = take_money(url2)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"1 European Euro = " + Eur)


@dp.message_handler(commands='Inline')
async def inline_kb(message: types.Message):
    await message.reply("Первая инлайн кнопка", reply_markup=inline_kb1)


button_usd = KeyboardButton('/Usd')
greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_usd)
button_eur = KeyboardButton('/Eur')
greet_kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_eur)
markup = ReplyKeyboardMarkup().add(button_usd).add(button_eur)

url1 = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=RUB'
url2 = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=EUR&To=RUB'
ua = UserAgent()

def take_money(url):
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    quest = soup.find('p', class_='result__BigRate-sc-1bsijpp-1 iGrAod')
    que = quest.text
    return que

@dp.message_handler(commands='Money')
async def takke_money(message: types.Message):
    await message.reply("Курсы валют, хорошо. Доллар или Евро?", reply_markup=inline_kb_full)

@dp.message_handler(commands='Usd')
async def take_usd(message: types.Message):
    Usd = take_money(url1)
    await message.reply("1 American Dollar = " + Usd)

@dp.message_handler(commands='Eur')
async def take_eur(message: types.Message):
    Eur = take_money(url2)
    await message.reply("1 European Euro = " + Eur)

if __name__ == '__main__':
    executor.start_polling(dp)