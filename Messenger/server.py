import json
import time
from datetime import datetime

from flask import Flask, request, abort

app = Flask(__name__)
load_time = datetime.now()

db = [
    {
        'text': 'Hello',
        'name': 'Molly',
        'time': time.time()
    }, {
        'text': 'Hello, Molly',
        'name': 'Paul',
        'time': time.time()
    }, {
        'text': 'How are you doing?',
        'name': 'Paul',
        'time': time.time()
    }
]


@app.route("/")
def hello():
    return "Hello, World! <a href='/status'>Statistics</a>"


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'LookUp',
        'time1': time.time(),
        'time2': time.asctime(),
        'time3': datetime.now().strftime('%Y/%m/%d %H:%M'),
        'time4': datetime.now(),
        'time5': str(datetime.now()),
        'time6': datetime.now().isoformat(),
        'time7 wrong': load_time
    }


@app.route("/send", methods=['POST'])
def send_message():
    print(request, json)
    if not isinstance(request.json, dict):
        return abort(400)

    text = request.json.get('text')
    name = request.json.get('name')
    if not isinstance(text, str) or not isinstance(name, str):
        return abort(400)
    if text == '' or name == '':
        return abort(400)

    db.append({
        'text': text,
        'name': name,
        'time': time.time()
    })
    return {'ok': True}


@app.route("/messages")
def get_messages():
    if 'after' in request.args:
        try:
            # format check
            after = float(request.args['after'])
        except:
            print('error')
            return
    else:
        # default behaviour
        after = 3

    filtered_db = []
    for message in db:
        if message['time'] > after:
            filtered_db.append(message)
            # pagination - to back messages by bunches
            if len(filtered_db) >= 100:
                break

    return {'messages': filtered_db}


app.run()

