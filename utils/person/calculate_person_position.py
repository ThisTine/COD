import requests
import asyncio
import threading

def calculate_person_position(bigBox: (int, int), smallBox: (int, int)):
    b_x1 = bigBox[0]
    b_x2 = bigBox[1]
    s_x1 = smallBox[0]
    s_x2 = smallBox[1]

    left = s_x1 - b_x1
    right = b_x2 - s_x2
    # print(requests.get("https://httpbin.org/get"))
    if left < 0 < right:
        thread = threading.Thread(target=asyncio.run, args=(cameraright(),))
        thread.start()
        return "LEFT"
    if right < 0 < left:
        thread = threading.Thread(target=asyncio.run, args=(cameraleft(),))
        thread.start()
        return "RIGHT"
    if left >= 0 and right >= 0:
        thread = threading.Thread(target=asyncio.run, args=(camerastop(),))
        thread.start()
        return "CENTER"
    if abs(left) - abs(right) > 0:
        thread = threading.Thread(target=asyncio.run, args=(cameraright(),))
        thread.start()
        return "LEFT"
    if abs(right) - abs(left) > 0:
        thread = threading.Thread(target=asyncio.run, args=(cameraleft(),))
        thread.start()
        return "RIGHT"
    response = requests.post("https://cod9000.pspgun.com/change/S",verify=False)
    return "CENTER"

    # return "LEFT"


async def cameraleft():
    requests.patch("https://cod9000.pspgun.com/change/L", verify=False)


async def cameraright():
    requests.patch("https://cod9000.pspgun.com/change/R", verify=False)


async def camerastop():
    requests.patch("https://cod9000.pspgun.com/change/S", verify=False)
