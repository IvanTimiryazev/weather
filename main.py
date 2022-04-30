import aiogram
import asyncio
from bs4 import BeautifulSoup
import requests
from config import BOT_TOKEN
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
import re

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
URL = 'https://weather.rambler.ru/v-sankt-peterburge/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36\
 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36', 'accept': '*/*'}


r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')
search = soup.find_all('div', class_="i81I")
for i in search:
        loc = i.find('div', class_="_33PN").text
        date = i.find('div', class_="_3hDK").text
        description = i.find('div', class_="Hixd").text
        temp_now = i.find('div', class_="_1HBR _3mFL").text
        feel = i.find('span', class_="UJ_C").text
temp_night = soup.find_all('div', class_="_3vZy _2Q4u")[0].text
temp_morning = soup.find_all('div', class_="_3vZy _2Q4u")[1].text
temp_day = soup.find_all('div', class_="_3vZy _2Q4u")[2].text


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        'Привет!' + '\n' + loc + ': ' + temp_now + '\n' + feel + '\n\n' + description
        + '\n\n' + 'Прогноз: ' + '\n' + temp_night + '\n' + temp_morning
        + '\n' + temp_day + '\n\n' + date)


executor.start_polling(dp, skip_updates=True)