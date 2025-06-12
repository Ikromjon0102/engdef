from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from utils.db_api.db import add_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = message.from_user
    await add_user(user.id, user.first_name, user.last_name)
    await message.answer(f"Salom, {user.full_name}!")
