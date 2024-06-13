from flask import Flask, redirect, url_for, render_template, request, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from engineio.async_drivers import threading


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret!"
socketio = SocketIO(
    app,
    async_mode="threading"
)

allConnection = []

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on('connect')
def connect():
    print("connect!")
    #allConnection.append(data.userId)
    # if(len(allConnection) == 1):
    #     emit("setting", "black")
    # else :
    #     emit("setting", "white")

@socketio.on('message')
def handle_message(data):
    print('received message: ', str(data))

@socketio.on('newLoc')
def newLoc(data):
    print("receive newLoc")
    

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

if(__name__ == "__main__") :
    socketio.run(app, allow_unsafe_werkzeug=True, host="0.0.0.0", port=8080)

def ack():
    print("message was received!")
