from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from random import random
from time import sleep
from threading import Thread, Event
import eventlet
eventlet.monkey_patch()
print("patched eventlet")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfg'
app.config['MONGO_URI'] = 'mongodb://localhost/RNoec2'
mongo = PyMongo(app)
socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def my_func():
    while True:
        eventlet.sleep(2)
        number = random()
        print(number)
        emit('numberg', {'number': number}, namespace='/test')
        mongo.db.dbs.insert_one({'no': number})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')