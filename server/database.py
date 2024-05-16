from secret import key
import sqlite3


# Note: an image file referencing the design of the database system and table relationships
# can be seen in this directory

# Note 2: running a SQL command follows the below syntax
'''
connection, cursor = create_connection()
command(cursor)
close_connection(connection, cursor)
'''


database_location = 'server/database.sqlite3'

# Initialises the connection, and returns the connection and cursor object
def create_connection():
    connection = sqlite3.connect(database_location)
    cursor = connection.cursor()

    return connection, cursor

def close_connection(connection, cursor):
    cursor.close()
    connection.close()


# Returns a string representing the date in ISO8601 format
# TODO
def get_datetime_string():
    date_time = ''
    return date_time



# Creating and deleting the database tables
def create_tables(cursor):
    cursor.execute('''CREATE TABLE Accounts(
                   PlayerID INTEGER PRIMARY KEY, 
                   Username TEXT NOT NULL, 
                   Password TEXT NOT NULL, 
                   ELO INTEGER NOT NULL, 
                   Date TEXT NOT NULL
                   );''')
    
    cursor.execute('''CREATE TABLE Sessions(
                   SessionID TEXT PRIMARY KEY,
                   PlayerID INTEGER NOT NULL, 
                   Date TEXT NOT NULL,
                   FOREIGN KEY(PlayerID) REFERENCES Accounts(PlayerID)
                   );''')
    
    cursor.execute('''CREATE TABLE Matches(
                   MatchID INTEGER PRIMARY KEY, 
                   Grid TEXT NOT NULL, 
                   Date TEXT NOT NULL
                   );''')
    
    cursor.execute('''CREATE TABLE Games(
                   GameID          INTEGER PRIMARY KEY,
                   PlayerID        INTEGER NOT NULL,
                   Grid            TEXT NOT NULL,
                   Time            TEXT NOT NULL,
                   Date            TEXT NOT NULL,
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

def reset_db(cursor):
    cursor.execute('DROP TABLE IF EXISTS MultiplayerResults')
    cursor.execute('DROP TABLE IF EXISTS Sessions')
    cursor.execute('DROP TABLE IF EXISTS Matches') #after MultiplayerResults
    cursor.execute('DROP TABLE IF EXISTS Games')
    cursor.execute('DROP TABLE IF EXISTS Accounts') #last

    create_tables(cursor)
    

# Returns a boolean specifying whether a username is taken
def check_username(cursor, username):

    query = cursor.execute('SELECT * FROM Accounts WHERE Username = ?', (username+'%',))
    return query.fetchone() is not None

# Adds a user to the database given username and password as inputs
def add_user(cursor, username, password):

    date_time = get_datetime_string()

    cursor.execute('INSERT INTO Accounts (Username, Password, ELO, Date) VALUES (?, ?, 1000, ?)', (username+'%',password+'%',date_time+'%'))


# Creates an account. Returns an error if the username is already in use
def create_account(username, password):
    hashed_password = hash(password + key)

    connection, cursor = create_connection()
    if not check_username(username): #username not in use
        add_user(cursor, username, hashed_password)
    else:
        raise Exception('Error: Username in use')

    close_connection(connection, cursor)

    attempt_login(username, password)

#TODO
# Attempts a login. Returns an error if the account doesn't exist or the password doesn't match
def attempt_login(username, password):

    if not check_username(username):
        raise Exception('Error: Username not found')

    hashed_password = hash(password + key)

    



#TODO
# Implement login
# Change name from session ID to "access token" idea
# Use tokens and whether they are expired as a method of logging in
# Finish the get time object and managing times