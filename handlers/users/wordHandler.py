from googletrans import Translator
import logging
from aiogram import types

from keyboards.inline.tarjimaKey import key
from utils.async_translate import async_translate
from utils.wordlookup import getdef
from loader import dp

translator = Translator()

# @dp.message_handler()
# async def tarjimon(message: types.Message):
#     lang = translator.detect(message.text).lang
#     if len(message.text.split()) > 1:
#         if lang == 'en':
#             dest = 'uz'
#             await message.answer(translator.translate(message.text, dest).text)
#         else:
#             await message.answer(translator.translate(message.text, dest='en').text)
#     else:
#         if lang == 'en':
#             word_id = message.text
#         else:
#             word_id = translator.translate(message.text, dest='en').text
#         lookup = getdef(word_id)
#         if lookup:
#             if lookup.get('audiouk'):# and lookup.get('audious'):
#                 await message.reply_voice(lookup['audiouk'], "United Kingdom version")
#                 # await message.reply_voice(lookup['audious'], "United Stated version")
#             await message.answer(f"Word: <b>{word_id.title()}</b>\nDefinitions:\n"
#                                  f"{lookup['definitions']}",reply_markup=key)
#         else:
#             await message.reply("Bunday so'z topilmadi")



# @dp.callback_query_handler(text="translate")
# async def tarjima(call: types.CallbackQuery):
#     msg = call.message.text
#     # logging.info(msg)
#     # await call.message.delete()
#     await call.message.answer(translator.translate(msg,dest='uz').text)
#     await call.answer(cache_time=60)


from aiogram import types
from loader import dp
from keyboards.inline.tarjimaKey import key

@dp.message_handler()
async def tarjimon(message: types.Message):
    text = message.text.strip()

    if not text:
        return await message.answer("Iltimos, tarjima uchun matn yuboring.")

    # Bir nechta so‘z bo‘lsa — to‘liq tarjima
    if len(text.split()) > 1:
        translated = await async_translate(text, target_lang='uz')
        return await message.answer(translated)

    # Bitta so‘z bo‘lsa — definitsiya olish
    translated_en = await async_translate(text, target_lang='en')
    definition_data = await getdef(translated_en)

    if definition_data:
        if definition_data.get("audiouk"):
            await message.reply_voice(definition_data['audiouk'], caption="🇬🇧 UK pronunciation")
        await message.answer(
            f"Word: <b>{translated_en.title()}</b>\nDefinitions:\n{definition_data['definitions']}",
            reply_markup=key
        )
    else:
        await message.answer("❌ Bunday so‘z topilmadi.")





from aiogram import types
from loader import dp
from utils.async_translate import async_translate

@dp.callback_query_handler(text="translate")
async def tarjima(call: types.CallbackQuery):
    msg = call.message.text
    translated = await async_translate(msg, target_lang='uz')
    await call.message.answer(translated)
    await call.answer(cache_time=60)