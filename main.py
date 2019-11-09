from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from random import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfg'
app.config['MONGO_URI'] = 'mongodb://localhost/RNoec2'
mongo = PyMongo(app)
socketio = SocketIO(app)


def random_no():
    return random()


@app.route('/')
def home():
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def my_func():
    number = random_no()
    emit('numberg', {'number' : number}, namespace='/test')
    mongo.db.dbs.insert({'no' : number})


socketio.run(app)