import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from routers import RouterFilm
import sqlite3

logging.basicConfig(level=logging.INFO)

bot = Bot(token="7516116342:AAGNe-5FKAzvbIRLtG8y2Zdgs6cmtM8CEMM")

pictures = {}
texts = {}

dp = Dispatcher()
dp.include_routers(RouterFilm.router)

kbs = {"start": types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="Фильмы")],
    [types.KeyboardButton(text="Что-то1")],
    [types.KeyboardButton(text="Что-то2")],
    [types.KeyboardButton(text="Что-то3")]], resize_keyboard=True),
}
form = ".png"

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать. Какой пост создаем?", reply_markup=kbs['start'])

@dp.message(Command('menu'))
async def menu(message: types.Message):
    await message.answer('Главное меню\nКакой пост делаем?', reply_markup=kbs['start'])
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
