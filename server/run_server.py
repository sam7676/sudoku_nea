from flask import Flask, request
from flask_socketio import SocketIO, send, emit
import threading

from aiohttp import web
import socketio

import database
from secret import flask_key


from collections import deque

queue = deque()


app = Flask(__name__)
app.config['SECRET_KEY'] = flask_key
socket = SocketIO(app)


# Checks whether a token is valid using database.py
@socket.on('check_token')
def check_token(json):
    token = json["token"]

    send({"result":database.check_access_token_validity(token)})

# Attempts to login
@socket.on('attempt_login')
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
@socket.on('attempt_register')
def attempt_register(json):
    username = json["username"]
    password = json["password"]

    try:
        playerID, token = database.create_account(username, password)
        send({"id":playerID, "token":token})
    except:
        print("Register failed")
        send({"id":None, "token":None})

@socket.on('submit_score')
def submit_score(json):

    id = json["playerID"]
    grid_time = json["grid_time"]
    grid_string = json["grid_string"]
    errors = json["errors"]
    hints = json["hints"]


    database.add_to_game(id, grid_string, grid_time, hints, errors)
    send({"id":None, "token":None})

@socket.on('get_leaderboard_data')
def get_leaderboard_data(json):

    name = json["name"]
    grid = json["grid"]

    data = database.send_leaderboard_data(name, grid)

    send({"result":data})



@socket.on('connect')
def connect(): 
    print("Connected")


@socket.on('disconnect')
def disconnect():
    print("Disconnected")



@socket.on('queue_multiplayer')
def queue_multiplayer(json):

    player_id = json["id"]
    socket_id = request.sid

    queue.append([player_id, socket_id])


@socket.on('win_game')
def win_game(json):

    match_id = json["match_id"]

    time = json["time"]

    my_socket = request.sid

    player1, player2, socket1, socket2 = database.get_match_details(match_id)

    if socket1 == my_socket:
        socket.emit("game_over", {"winner":False}, to=socket2)
        socket.emit("game_over", {"winner":True}, to=socket1)

        player1_elo = database.get_player_elo(player1)
        player2_elo = database.get_player_elo(player2)

        new_p1_elo, new_p2_elo = update_ELO(player1_elo, player2_elo, win=1)



        database.log_multiplayer_result(player1, match_id, player1_elo, new_p1_elo, time, win=True)
        database.log_multiplayer_result(player2, match_id, player2_elo, new_p2_elo, time, win=False)

    else:
        socket.emit("game_over", {"winner":False}, to=socket1)
        socket.emit("game_over", {"winner":True}, to=socket2)

        player1_elo = database.get_player_elo(player1)
        player2_elo = database.get_player_elo(player2)

        new_p1_elo, new_p2_elo = update_ELO(player1_elo, player2_elo, win=2)

        database.log_multiplayer_result(player2, match_id, player2_elo, new_p2_elo, time, win=True)
        database.log_multiplayer_result(player1, match_id, player1_elo, new_p1_elo, time, win=False)



def host_queue():

    while True:

        if len(queue) >= 2:

            player_id_1, socket_id_1 = queue.popleft()
            player_id_2, socket_id_2 = queue.popleft()

            match_id, grid = database.create_match(player_id_1, player_id_2, socket_id_1, socket_id_2)

            socket.emit("game_start", {"match_id":match_id, "grid":grid}, to=socket_id_1)
            socket.emit("game_start", {"match_id":match_id, "grid":grid}, to=socket_id_2)


def update_ELO(rating1, rating2, win=1):

    # Probability of someone winning
    P1 = (1.0 / (1.0 + pow(10, ((rating1 - rating2) / 400)))); 
    P2 = (1.0 / (1.0 + pow(10, ((rating2 - rating1) / 400)))); 

    # Case -1 When Player A wins
    # Updating the Elo Ratings
    if (win == 1):
        rating1 = rating1 + 50 * (1 - P1)
        rating2 = rating2 + 50 * (0 - P2)
 
    # Case -2 When Player B wins
    # Updating the Elo Ratings
    else:
        rating1 = rating1 + 50 * (0 - P1)
        rating2 = rating2 + 50 * (1 - P2)
 
    return (rating1, rating2)




if __name__ == '__main__':


    # Hosting the synchronous socket on one thread and the game pairing queue on the other
    thread1 = threading.Thread(target=socket.run, args=(app,))

    thread2 = threading.Thread(target=host_queue)


    thread1.start()
    thread2.start()
