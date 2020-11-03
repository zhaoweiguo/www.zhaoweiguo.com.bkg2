#!/usr/bin/python
# coding: utf8

import time
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import json
from datetime import timedelta
import subprocess


app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=1)
app.config["threaded"] = True

#socketio = SocketIO(app)

@app.route('/', methods=['POST'])
def hook():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        branch = json_data["branch"]
        print(branch)

        return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, threaded=True)



