from secret import key
import sqlite3
import datetime
import hashlib #Python's hash function is non-deterministic, so this is necessary
import random
import os
import grid_generator

# Note 1: an image file referencing the design of the database system and table relationships
# can be seen in this directory
# Note 2: running a SQL command follows the below syntax
'''
connection, cursor = create_connection()
command(cursor)
close_connection(connection, cursor)
'''
# Note 3: a function includes cursor as a parameter only if it is a helper function


database_location = 'server/database.sqlite3'

# Initialises the connection, and returns the connection and cursor object
def create_connection():
    connection = sqlite3.connect(database_location)
    cursor = connection.cursor()

    return connection, cursor

def close_connection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()



# Returns a string representing the date in ISO8601 format
def get_date():
    return str(datetime.datetime.now(datetime.timezone.utc))

# Used for manipulating times, takes ISO8601 format string as input and outputs a DateTime object
def get_DateTime_object(dt_string):
    dt = datetime.datetime.fromisoformat(dt_string)
    return dt



# Generates a potential access token. Collisions are EXTREMELY unlikely (< 1 / 2**200) 
# however countermeasures are brought in regardless.
def generate_token():

    return ''.join(chr(random.randint(33,125)) for i in range(32))



# Returns a hash for our password using salt and pepper hashing
def hash_password(password):
    return hashlib.sha256((str(len(password)) + str(len(password)-1) + password + key).encode()).hexdigest()



# Creating and deleting the database tables
def create_db():

    connection, cursor = create_connection()

    cursor.execute('''CREATE TABLE Accounts(
                   PlayerID INTEGER PRIMARY KEY, 
                   Username TEXT NOT NULL, 
                   Password TEXT NOT NULL, 
                   ELO INTEGER NOT NULL, 
                   Date TEXT NOT NULL
                   );''')
    
    cursor.execute('''CREATE TABLE AccessTokens(
                   AccessToken TEXT PRIMARY KEY,
                   PlayerID INTEGER NOT NULL, 
                   Date TEXT NOT NULL,
                   FOREIGN KEY(PlayerID) REFERENCES Accounts(PlayerID)
                   );''')
    
    # This breaks normalisation
    cursor.execute('''CREATE TABLE Matches(
                   MatchID INTEGER PRIMARY KEY, 
                   Grid TEXT NOT NULL, 
                   Date TEXT NOT NULL,
                   Player1 INTEGER NOT NULL,
                   Player2 INTEGER NOT NULL,
                   Socket1 TEXT NOT NULL,
                   Socket2 TEXT NOT NULL
                   );''')
    
    cursor.execute('''CREATE TABLE Games(
                   GameID          INTEGER PRIMARY KEY,
                   PlayerID        INTEGER NOT NULL,
                   Grid            TEXT NOT NULL,
                   Time            TEXT NOT NULL,
                   Date            TEXT NOT NULL,
                   Hints           INTEGER NOT NULL,
                   Errors          INTEGER NOT NULL,
                   FOREIGN KEY(PlayerID) REFERENCES Accounts(PlayerID)
                   );''')
    
    cursor.execute('''CREATE TABLE MultiplayerResults(
                   MultiplayerID   INTEGER PRIMARY KEY,
                   MatchID         INTEGER NOT NULL,
                   PlayerID        INTEGER NOT NULL,
                   Time            TEXT NOT NULL,
                   OldELO          INTEGER NOT NULL,
                   NewELO          INTEGER NOT NULL,
                   Winner          INTEGER NOT NULL,
                   FOREIGN KEY(MatchID) REFERENCES Accounts(MatchID),
                   FOREIGN KEY(PlayerID) REFERENCES Accounts(PlayerID)
                   );''')
    
    close_connection(connection, cursor)

def reset_db():

    connection, cursor = create_connection()

    # Deleting old
    cursor.execute('DROP TABLE IF EXISTS MultiplayerResults')
    cursor.execute('DROP TABLE IF EXISTS AccessTokens')
    cursor.execute('DROP TABLE IF EXISTS Matches') #after MultiplayerResults
    cursor.execute('DROP TABLE IF EXISTS Games')
    cursor.execute('DROP TABLE IF EXISTS Accounts') #last

    close_connection(connection, cursor)

    create_db()




# Returns a boolean specifying whether a username is taken
def check_username(cursor, username):

    query = cursor.execute('SELECT * FROM Accounts WHERE Username = ?', (username,))
    return query.fetchone() is not None

# Returns a boolean specifying whether a login is correct
def check_login(cursor, username, password):

    query = cursor.execute('SELECT * FROM Accounts WHERE Username = ? AND Password = ?', (username,password,))
    return query.fetchone()

# Adds a user to the database given username and password as inputs
def add_user(cursor, username, password):

    date = get_date()

    cursor.execute('INSERT INTO Accounts (Username, Password, ELO, Date) VALUES (?, ?, 1000, ?)', (username,password,date))



# Creates an account. Returns an error if the username is already in use
def create_account(username, password):

    hashed_password = hash_password(password)

    connection, cursor = create_connection()
    if not check_username(cursor, username): #username not in use
        add_user(cursor, username, hashed_password)
    else:
        raise Exception('Error: Username in use')

    close_connection(connection, cursor)

    return attempt_login(username, password)

# Attempts a login. Returns an error if the account doesn't exist or the password doesn't match
def attempt_login(username, password):

    connection, cursor = create_connection()

    if not check_username(cursor, username):
        raise Exception('Error: Username not found')

    hashed_password = hash_password(password)

    login_attempt = check_login(cursor, username, hashed_password)

    if login_attempt is not None:

        playerID = login_attempt[0]

        token = create_access_token(cursor, playerID)

    else:
        raise Exception('Error: Password incorrect')

    close_connection(connection, cursor)

    return (playerID, token)



# Returns a boolean specifying whether a token has been used before
def is_access_token_used(cursor, token):


    query = cursor.execute('SELECT * FROM AccessTokens WHERE AccessToken = ?', (token,))
    return query.fetchone() is not None

# Returns a boolean specifying whether a token is valid, and if so the playerID
def check_access_token_validity(token):

    connection, cursor = create_connection()
    if not is_access_token_used(cursor, token):

        close_connection(connection, cursor)
        return None
    
    else:
        query = cursor.execute('SELECT * FROM AccessTokens WHERE AccessToken = ?', (token,))

        result = query.fetchone()

        date = get_DateTime_object(result[2])

        past = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)

        if date >= past:
            playerID = result[1]
            close_connection(connection, cursor)
            return playerID

        else:
            close_connection(connection, cursor)
            return None

# Creates a new access token and allocates it to a given user
def create_access_token(cursor, playerID):

    date = get_date()

    token = generate_token()
    while is_access_token_used(cursor, token):
        token = generate_token()

    cursor.execute('INSERT INTO AccessTokens (AccessToken, PlayerID, DATE) VALUES (?, ?, ?)', (token, playerID, date))

    return token


def add_to_game(playerID, grid, time, hints, errors):

    connection, cursor = create_connection()

    cursor.execute('INSERT INTO Games (PlayerID, Grid, Time, Date, Hints, Errors) VALUES (?, ?, ?, ?, ?, ?)', 
                   (playerID, grid, time, get_date(), hints, errors))

    close_connection(connection, cursor)
    

def get_username(cursor, playerID):

    query = cursor.execute('SELECT Username FROM Accounts WHERE PlayerID = ?', (playerID,))

    return query.fetchone()[0]


def send_leaderboard_data(name, grid):

    connection, cursor = create_connection()

    #TODO
    
    if grid == '':
        grid = '%'

    query = cursor.execute(
    'SELECT Accounts.Username, Games.Grid, Games.Time, Games.Date, Games.Hints, Games.Errors FROM Accounts INNER JOIN Games ON Accounts.PlayerID = Games.PlayerID WHERE Accounts.Username LIKE ? AND Games.Grid LIKE ? ORDER BY Games.Time',
            (name+'%', grid))


    result = query.fetchmany(15)

    close_connection(connection, cursor)

    return result




def create_match(player_id_1, player_id_2, socket_id_1, socket_id_2):

    connection, cursor = create_connection()

    grid = grid_generator.generate([100, 2]).ans

    cursor.execute('INSERT INTO Matches (Grid, Date, Player1, Player2, Socket1, Socket2) VALUES (?, ?, ?, ?, ?, ?)', 
                   (grid, get_date(), player_id_1, player_id_2, socket_id_1, socket_id_2))

    match_id = cursor.lastrowid

    close_connection(connection, cursor)

    return match_id, grid

def get_match_details(match_id):

    connection, cursor = create_connection()

    query = cursor.execute('SELECT Player1, Player2, Socket1, Socket2 FROM Matches WHERE MatchID = ?', (match_id,))

    result = query.fetchone()

    close_connection(connection, cursor)

    return result


def log_multiplayer_result(player_id, match_id, old_elo, new_elo, time, win):

    connection, cursor = create_connection()

    win = 1 if win else 0

    cursor.execute('INSERT INTO MultiplayerResults (MatchID, PlayerID, Time, OldELO, NewELO, Winner) VALUES (?, ?, ?, ?, ?, ?)', 
                   (match_id, player_id, time, old_elo, new_elo, win))

    close_connection(connection, cursor)


def get_player_elo(player_id):

    connection, cursor = create_connection()

    query = cursor.execute('SELECT ELO FROM Accounts WHERE PlayerID = ?', (player_id,))

    result = query.fetchone()[0]

    close_connection(connection, cursor)

    return result



if not os.path.exists(database_location):
    create_db()