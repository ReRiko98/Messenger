import requests

name = input('Write a name: ')

while True:
    text = input()
    requests.post('http://127.0.0.1:5000/send', json={
        'name': name,
        'text': text
    })