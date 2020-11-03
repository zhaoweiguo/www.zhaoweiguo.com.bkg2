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

# 实例：
# {
#    "path":"/var/www/zhaoweiguo.com/www.zhaoweiguo.com", 
#    "branch": "master", 
#    "actions": [pull, make, make clean]
#}
@app.route('/', methods=['POST'])
def hook():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    branch = json_data["branch"]
    print(branch)
    actions = json_data["actions"]
    path = json_data["path"]
    if path=="":
        path = "/var/www/zhaoweiguo.com/www.zhaoweiguo.com"
    print(path)
    print(actions)

    if 'pull' in actions:
        print("[run]pull")
        subprocess.Popen("git pull origin master &>> /tmp/hook.log &", cwd=path, shell=True, stdout=subprocess.PIPE).communicate()
    if 'make clean' in actions:
        print("[run]make clean")
        subprocess.Popen("make clean &>> /tmp/hook.log &", cwd=path, shell=True, stdout=subprocess.PIPE).communicate()
    if 'make' in actions:
        print("[run]make")
        subprocess.Popen("make &>> /tmp/hook.log &", cwd=path, shell=True, stdout=subprocess.PIPE).communicate()

    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, threaded=True)



