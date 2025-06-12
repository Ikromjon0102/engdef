import requests
from json import loads
import json

# def getdef(word_id):
#     # url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + word_id.lower()
#     url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word_id.lower()
#     r = requests.get(url)
#     res = r.json()
#
#     if str(type(res)) == "<class 'list'>":
#         output = {}
#         sensess = res[0].get("meanings")
#
#         definition = []
#         for i in range(len(sensess)):
#             definition.append(f"\n<i><b>Part of speech - {sensess[i].get('partOfSpeech')}</b></i>\n")
#             for sense in sensess[i].get("definitions"):
#                 definition.append(f"👉 <b>{word_id.title()}</b> - {sense['definition']}")
#         output['definitions'] = "\n".join(definition)
#         output['audiouk'] = res[0].get("phonetics")[0].get("audio")
#         # output['audious'] = res[0].get("phonetics")[1].get("audio")
#
#         return output
#     else:
#         return False
    # return res[0].get("phonetics")[0].get("audio")
#

import aiohttp

async def getdef(word: str):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return False

                res = await response.json()

                if isinstance(res, list):
                    output = {}
                    senses = res[0].get("meanings", [])
                    definition = []

                    for item in senses:
                        pos = item.get("partOfSpeech", "unknown")
                        definition.append(f"\n<i><b>Part of speech - {pos}</b></i>\n")
                        for sense in item.get("definitions", []):
                            definition.append(f"👉 <b>{word.title()}</b> - {sense['definition']}")

                    output['definitions'] = "\n".join(definition)

                    # Audio (UK/US)
                    phonetics = res[0].get("phonetics", [])
                    audio_url = None
                    for p in phonetics:
                        if p.get("audio"):
                            audio_url = p['audio']
                            break

                    output['audiouk'] = audio_url
                    return output

                return False

    except Exception as e:
        print(f"Xatolik: {e}")
        return False



if __name__ == '__main__':
    from pprint import pprint as print
    print(getdef("apple"))
#     # print(getdef("america"))