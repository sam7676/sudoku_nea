from flask import Flask
from flask_socketio import SocketIO, send, emit


import database
from secret import flask_key


app = Flask(__name__)
app.config['SECRET_KEY'] = flask_key
socketio = SocketIO(app)


# Checks whether a token is valid using database.py
@socketio.on('check_token')
def check_token(json):
    token = json["token"]

    send({"result":database.check_access_token_validity(token)})

# Attempts to login
@socketio.on('attempt_login')
def attempt_login(json):
    username = json["username"]
    password = json["password"]

    try:
        playerID, token = database.attempt_login(username, password)
        send({"id":playerID, "token":token})
    except:
        print("Login failed")
        send({"id":None, "token":None})

# Attempts to login
@socketio.on('attempt_register')
def attempt_register(json):
    username = json["username"]
    password = json["password"]

    try:
        playerID, token = database.create_account(username, password)
        send({"id":playerID, "token":token})
    except:
        print("Register failed")
        send({"id":None, "token":None})

@socketio.on('submit_score')
def submit_score(json):
    print(json)



@socketio.on('connect')
def connect():
    print("connected")

@socketio.on('disconnect')
def disconnect():
    print("disconnected")


if __name__ == '__main__':
    socketio.run(app)