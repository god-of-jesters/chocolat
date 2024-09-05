import os
from aiogram import Router, F, Bot
from aiogram import types
from aiogram.enums import ParseMode

kbs = {"start": types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="Фильмы")],
    [types.KeyboardButton(text="Что-то1")],
    [types.KeyboardButton(text="Что-то2")],
    [types.KeyboardButton(text="Что-то3")]], resize_keyboard=True),
}

router = Router()
step = ''
pictures = {}
post = ''
kb = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text='/menu')],
    [types.KeyboardButton(text='Пропустить')]
], resize_keyboard=True)
fragments_text = []

@router.message(F.text.lower() == 'фильмы')
async def director(message: types.Message):
    global step
    step = 'first'
    await message.answer('Имя файла', reply_markup=kb)

@router.message(F.photo)
async def dowload_pic(message: types.Message, bot: Bot):
    global step
    step = 'photo'
    await bot.download(message.photo[-1], destination=f"{pictures[message.chat.id]}.png")
    await message.answer("Загрузил")
    await message.answer('Название ссылка на фильм')

@router.message(F.text)
async def text_handler(message: types.Message, bot: Bot):
    global step, post, fragments_text
    text = message.text
    fragments_text = []
    steps = ['first', 'photo', 'film name', 'director', 'year', 'Djone', "Can't", 'risk', 'if', 'go', 'u say']
    if step == 'first':
        step = 'name'
        pictures[message.chat.id] = text
        await message.answer('Жду фоточку')
    elif step == 'photo':
        step = 'film name'
        fragments_text = text.split()
        post = post + '<a href="' + fragments_text[-1] + '">' + ' '.join(
            fragments_text[:len(fragments_text) - 1]) + '</a>\n' + '\n'
        await message.answer('Имя Фамилия ссылка режисера')
    elif step == 'film name':
        step = 'director'
        fragments_text = text.split()
        post = post + 'Режиссёр: ' + '<a href="' + fragments_text[-1] + '">' + ' '.join(
            fragments_text[:len(fragments_text) - 1]) + '</a> \n'
        await message.answer('Год выхода')
    elif step == 'director':
        step = 'year'
        post = post + 'Год выхода: ' + text + '\n\n'
        await message.answer('🧐 Ничего ты не знаешь, Джон Сноу')
    elif step == 'year':
        step = 'Djone'
        post = post + '🧐 <b>Ничего ты не знаешь, Джон Сноу!</b> \n\n' + '— ' + text + '\n\n'
        await message.answer('🤯 Нельзя просто так взять и…')
    elif step == 'Djone':
        step = "Can't"
        post = post + '🤯 <b>Нельзя просто так взять и…</b>\n\n' + '— ' + text + '\n\n'
        await message.answer('😈 Я тоже люблю рисковать')
    elif step == "Can't":
        step = 'risk'
        post = post + '😈 <b>Я тоже люблю рисковать</b>\n\n' + '— ' + text + '\n\n'
        await message.answer('🤔 А что, если…')
    elif step == 'risk':
        step = 'if'
        post = post + '🤔 <b>А что, если…</b>\n\n' + '— ' + text + '\n\n'
        await message.answer('🤬 Ну да, ну да, пошёл я нафиг')
    elif step == 'if':
        step = 'go'
        post = post + '🤬 <b>Ну да, ну да, пошёл я нафиг</b>\n\n' + '— ' + text + '\n\n'
        await message.answer('😎 А теперь ты приходишь и говоришь…')
    elif step == 'go':
        step = 'u say'
        post = post + '😎 <b>А теперь ты приходишь и говоришь…</b>\n\n' + '— ' + text + '\n\n'
        await message.answer('😌 Знаете, я и сам своего рода…')
    elif step == 'u say':
        step = 'u cam'
        post = post + '😌 <b>Знаете, я и сам своего рода…</b>\n\n' + '— ' + text + '\n\n❤️ – смотрели\n🔥 – уже загружаем\n\n#фильмиус'
        await message.answer('пост закончен')
        photo = types.FSInputFile(f"{pictures[message.chat.id]}.png")
        await bot.send_photo(message.chat.id, photo=photo, caption=post, parse_mode=ParseMode.HTML)
        os.remove(f'C:/Users/dimasik/kir_bot/Content_bot/{pictures[message.chat.id]}.png')
        await message.answer('Главное меню\nКакой пост делаем?', reply_markup=kbs['start'])
