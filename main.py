from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from random import random
from time import sleep
from threading import Thread, Event

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfg'
app.config['MONGO_URI'] = 'mongodb://localhost/RNoec2'
mongo = PyMongo(app)
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()
class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()
    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print("Making random numbers")
        while not thread_stop_event.isSet():
            number = round(random()*10, 3)
            print(number)
            socketio.emit('numberg', {'number': number}, namespace='/test')
            mongo.db.dbs.insert_one({'no': number})
            sleep(self.delay)
    def run(self):
        self.randomNumberGenerator()


@app.route('/')
def home():
    return render_template('index.html')


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


@socketio.on('connect', namespace='/test')
def my_func():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()


socketio.run(app)