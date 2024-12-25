import requests


def translate_text_mymemory(text: str, source_lang: str, target_lang: str) -> str | None:
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"{source_lang}|{target_lang}"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["responseData"]["translatedText"]
    else:
        print("Ошибка:", response.status_code)
        return None