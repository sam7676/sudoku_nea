
# from ..server import database

import os 
print(os.getcwd())

#TODO
def read_token():
    file = open('access_token.txt','r')
    line = file.readline()
    print(line)

#TODO
def write_token(token):
    pass


# Checks whether the access token is valid
def check_token(access_token):

    valid = False
    try:
        valid = database.check_access_token_validity(access_token)
    except: pass

    return valid

#TODO
def attempt_login(username, password):
    playerID, token = database.attempt_login(username, password)
    write_token(token)

