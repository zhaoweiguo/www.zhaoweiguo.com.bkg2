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
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    branch = json_data["branch"]
    print(branch)
    force = json_data["force"]
    path = json_data["path"]
    if path=="":
        path = "/var/www/zhaoweiguo.com/www.zhaoweiguo.com"
    if force==True:
        force = True

    subprocess.Popen("git pull origin master &> /tmp/abc.log &", cwd=path, shell=True, stdout=subprocess.PIPE).communicate()
    if force:
        subprocess.Popen("make clean && make &> /tmp/abc.log &", cwd=path, shell=True, stdout=subprocess.PIPE).communicate()



    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, threaded=True)



