import aiohttp

async def async_translate(text: str, target_lang: str = 'en', source_lang: str = 'auto') -> str:
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        'client': 'gtx',
        'sl': source_lang,
        'tl': target_lang,
        'dt': 't',
        'q': text,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                return "Tarjima qilishda xatolik yuz berdi."
            data = await resp.json()
            # print(data, len(data), type(data))
            datas = [i[0] for i in data[0]]
            text = " ".join(datas)
            # print(text)
            # strp = 1
            # for i in data[0]:
            #     print(f"{strp} - {i}\n\n")
            #     strp += 1
            return text  # Asosiy tarjima qismi
