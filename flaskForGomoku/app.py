from flask import Flask, redirect, url_for, render_template, request, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from engineio.async_drivers import threading
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret!"
socketio = SocketIO(
    app,
    async_mode="threading"
)
user_name = ""

allConnection = []

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/submit", methods = ["POST"])
def submit():
    session["user_name"] = request.form["userName"]
    print(user_name)
    return redirect(url_for("gomoku"))

@app.route("/gomoku")
def gomoku():
    return render_template("index.html", userName = session["user_name"])

@socketio.on('connect')
def connect():
    print("connect!")

@socketio.on('join')
def join(data):
    print("join room!", str(data), data["userId"])
    if(len(allConnection) == 0):
        room = data["userId"]
        join_room(room)
        allConnection.append(room)
        emit('setting', {"color": "black", "status": "wait for opponent"}, to=allConnection[0])
    elif(len(allConnection) == 1):
        room = data["userId"]
        join_room(room)
        allConnection.append(room)
        emit('setting', {"color": "white", "status": "wait for opponent"}, to=allConnection[1])
        emit('start', to=allConnection[0])
        emit('start', to=allConnection[1])

@socketio.on('message')
def handle_message(data):
    print('received message: ', str(data))

@socketio.on('newLoc')
def newLoc(data):
    print("receive newLoc from", data["userId"])
    if(data["userId"] == allConnection[0]):
        emit('newLoc', data, to=allConnection[1])
    elif(data["userId"] == allConnection[1]):
        emit('newLoc', data, to=allConnection[0])
    

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

if(__name__ == "__main__") :
    socketio.run(app, allow_unsafe_werkzeug=True, host="0.0.0.0", port=8080)

def ack():
    print("message was received!")
