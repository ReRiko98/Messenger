import time
from datetime import datetime

import requests


def print_message(message):
    beauty_time = datetime.fromtimestamp(message['time'])
    beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M')
    print(beauty_time, message['name'])
    print(message['text'])
    print()


after = 3

while True:
    response = requests.get(
       'http://127.0.0.1:5000/messages?after=' + str(after)
    )
    for message in response.json()['messages']:
        dt = datetime.fromtimestamp(message['time'])
        dt = dt.strftime('%Y/%m/%d %H:%M')

        print(dt, message['name'])
        print(message['text'])
        print()

        after = message['time']

    time.sleep(1)
