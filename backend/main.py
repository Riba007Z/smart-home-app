from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from websocket_manager import connect, disconnect

from knx import start_knx, stop_knx, xknx, get_states
from xknx.tools import group_value_write

from onehome import get_devices

from fastapi.middleware.cors import CORSMiddleware

from slovenian_voice import get_text


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    #allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DeviceCommand(BaseModel):
    address: str
    value: bool


class VoiceCommand(BaseModel):
    text: str



devices_cache = []



@app.on_event("startup")
async def startup():

    global devices_cache

    await start_knx()

    devices_cache = get_devices()

    print("Loaded devices:")
    print(devices_cache)



@app.on_event("shutdown")
async def shutdown():

    await stop_knx()



@app.get("/")
def home():

    return {
        "status": "running"
    }



@app.post("/device")
def device(command: DeviceCommand):

    group_value_write(
        xknx,
        command.address,
        command.value
    )

    return {
        "address": command.address,
        "value": command.value
    }



@app.get("/devices")
def devices():

    return get_devices()



@app.get("/states")
def states():

    return get_states()



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await connect(websocket)

    try:

        while True:
            await websocket.receive_text()

    except:

        disconnect(websocket)




# ---------------- VOICE ----------------


def normalize_slovenian(text):

    replacements = {
        "č": "c",
        "š": "s",
        "ž": "z",
    }

    for old, new in replacements.items():

        text = text.replace(old, new)

    return text




def clean_voice_text(text):

    text = text.lower()

    text = normalize_slovenian(text)


    replacements = {

        # speech recognition mistakes

        "prizki": "prizgi",
        "prizge": "prizgi",
        "prizg": "prizgi",

        "vklopi": "vklopi",
        "ugasni": "ugasni",

    }


    for old, new in replacements.items():

        text = text.replace(old, new)


    return text




def normalize_numbers(text):

    numbers = {

        "ena": "1",
        "eno": "1",
        "en": "1",

        "dve": "2",
        "dva": "2",

        "tri": "3",

        "stiri": "4",

        "pet": "5",

        "sest": "6",

        "sedem": "7",

        "osem": "8",

        "devet": "9",

        "nic": "0",
        "nc": "0",
    }


    words = text.split()


    return " ".join(
        numbers.get(word, word)
        for word in words
    )




def join_numbers(text):

    words = text.split()


    known_words = []


    for device in devices_cache:

        known_words.append(
            normalize_slovenian(
                device["name"].lower()
            )
        )


        known_words.append(
            normalize_slovenian(
                device["room"].lower()
            )
        )


    result = []

    i = 0


    while i < len(words):


        if i + 1 < len(words):

            combined = words[i] + words[i+1]


            if combined in known_words:

                result.append(combined)

                i += 2
                continue


        result.append(words[i])

        i += 1


    return " ".join(result)




def search_device(text):

    for device in devices_cache:


        name = normalize_slovenian(
            device["name"].lower()
        )


        room = normalize_slovenian(
            device["room"].lower()
        )


        if name in text and room in text:

            return device



    return None




def find_device(text):

    text = clean_voice_text(text)


    print("CLEAN TEXT:", text)



    # try normal

    device = search_device(text)


    if device:

        return device



    # convert numbers

    text = normalize_numbers(text)


    print("NUMBER TEXT:", text)



    # join "luc 1" -> "luc1"

    text = join_numbers(text)


    print("JOIN TEXT:", text)



    device = search_device(text)


    if device:

        return device



    return None





@app.post("/voice")
def voice(command: VoiceCommand):


    text = clean_voice_text(command.text)


    print("VOICE:", text)



    device = find_device(text)



    if not device:

        return {

            "error": "Device not found",

            "text": text

        }




    if (

        "on" in text

        or "prizgi" in text

        or "vklopi" in text

    ):

        value = True



    elif (

        "off" in text

        or "ugasni" in text

        or "izklopi" in text

    ):

        value = False



    else:

        return {

            "error": "unknown action",

            "text": text

        }




    group_value_write(

        xknx,

        device["groupAddress"],

        value

    )



    return {

        "device": device["name"],

        "room": device["room"],

        "address": device["groupAddress"],

        "value": value

    }
    
@app.get("/listen")
def listen():

    text = get_text()

    return {
        "text": text
    }