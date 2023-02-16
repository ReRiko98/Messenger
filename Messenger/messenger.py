from datetime import datetime

import requests
from PyQt6 import QtWidgets, QtCore

import clientui


class MessengerWindow(QtWidgets.QMainWindow, clientui.Ui_Messenger):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)

        self.url = url

        self.SendButton.pressed.connect(self.send_message)

        self.after = 3
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def update_messages(self):
        response = requests.get(
            self.url + 'messages',
            params={'after': self.after}
        )
        for message in response.json()['messages']:
            dt = datetime.fromtimestamp(message['time'])
            dt = dt.strftime('%Y/%m/%d %H:%M')

            self.messagesBrowser.append(dt + ' ' + message['name'])
            self.messagesBrowser.append(message['text'])
            self.messagesBrowser.append('')

            self.after = message['time']

    def send_message(self):
        name = self.nameinput.text()
        text = self.textinput.toPlainText()
        try:
            response = requests.post(
                self.url + 'send',
                json={'text': text, 'name': name}
            )

        except:
            self.messagesBrowser.append("Server is not available. Try later")
            self.messagesBrowser.append('')
            self.messagesBrowser.repaint()
            return

        if response.status_code == 400:
            self.messagesBrowser.append("Wrong name/password")
            self.messagesBrowser.append('')
            self.messagesBrowser.repaint()
            return

        self.textinput.clear()
        self.textinput.repaint()


app = QtWidgets.QApplication([])
window = MessengerWindow('https://3871fb97a52f.ngrok.io/')
window.show()
app.exec()