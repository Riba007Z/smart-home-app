import requests

from slovenian_voice import get_text


while True:

    text = get_text()


    if not text:
        continue


    response = requests.post(
        "http://192.168.64.110:8000/voice",
        json={
            "text":text
        }
    )


    print(
        "Assistant:",
        response.json()
    )