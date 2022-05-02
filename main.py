import os
import aiogram
import asyncio
from bs4 import BeautifulSoup
import requests
from config import BOT_TOKEN, URL_APP
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


async def on_startup(_):
    print('Bot online')
    # await bot.set_webhook(URL_APP)  #ЭТО ДЛЯ ЗАПУСКА ВЭБ ХУКА
# async def on_shutdown(dp):
#     await bot.delete_webhook()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('<b>Привет!</b> \nЭто бот погоды.\n\nВведи название своего города <b>транслитом:</b>')


@dp.message_handler()
async def weather(message: types.Message):
    URL = f'https://weather.rambler.ru/v-{message.text}e/'
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
    await message.answer(
        loc + ': ' + temp_now + '\n' + feel + '\n\n' + description
        + '\n\n' + 'Прогноз: ' + '\n' + temp_night + '\n' + temp_morning
        + '\n' + temp_day + '\n\n' + date + '\n' + 'Хорошего дня!❤')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
# executor.start_webhook(
#     dispatcher=dp,
#     webhook_path='',
#     on_startup=on_startup,
#     on_shutdown=on_shutdown,
#     skip_updates=True,
#     host="0.0.0.0",
#     port=int(os.environ.get("PORT", 5000)))