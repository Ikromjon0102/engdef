from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, bot
from utils.db_api.db import add_user, get_users_count, get_users


@dp.message_handler(commands="count")
async def bot_start(message: types.Message):
    user = message.from_user
    a = await get_users_count()
    await message.answer(f"Assalomu aleykum, botning jami foydalanuvchilari soni {a} taga yetdi!")


# @dp.message_handler(commands="msg")
# async def bot_start(message: types.Message):
#     # user = message.from_user
#     users = await get_users()
#     for i in users:
#         await bot.send_message(i, "salom hammaga")
#     # await message.answer(f"Assalomu aleykum, botning jami foydalanuvchilari soni {a} taga yetdi!")

from aiogram import types
from aiogram.dispatcher.filters import Command

# Adminlar ro‘yxati
ADMIN_IDS = [984106361, 92473435]

@dp.message_handler(Command("msg"))
async def broadcast_message(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.reply("⛔ Sizga bu komanda ruxsat etilmagan.")

    # Buyruqdan keyingi matnni ajratish
    text = message.text.partition(" ")[2].strip()

    if not text:
        await message.reply("❗ Iltimos, xabar matnini ham yozing. Masalan:\n`/msg Bugun dars bo‘lmaydi`", parse_mode="Markdown")
        return

    # Foydalanuvchilar ro‘yxati
    user_ids = await get_users()

    sent = 0
    failed = 0

    for user_id in user_ids:
        try:
            await bot.send_message(user_id, text, parse_mode="HTML")
            sent += 1
        except Exception as e:
            failed += 1
            # print(f"⚠️ {user_id} ga yuborib bo‘lmadi: {e}")

    await message.answer(
        f"📢 Xabar yuborildi!\n✅ Yuborildi: {sent} ta\n❌ Yuborilmagan: {failed} ta"
    )

