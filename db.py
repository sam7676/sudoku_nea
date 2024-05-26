from imports import *


def add_result(name,grid,date,time):
    con = sqlite3.connect(database_location)
    cur = con.cursor()

    cur.execute("INSERT INTO results VALUES (?, ?, ?, ?)",(name,grid,date,time,))
    con.commit()

    cur.close()
    con.close()

def search_result(name,grid):
    con = sqlite3.connect(database_location)
    cur = con.cursor()

    k = cur.execute('''SELECT * FROM results WHERE name LIKE ? AND grid LIKE ? ORDER BY time''',(name+'%',grid+'%',))
    result = k.fetchmany(15)
    cur.close()
    con.close()
    return result
    

def create_db_table():
    con = sqlite3.connect(database_location)
    cur = con.cursor()
    cur.execute("CREATE TABLE results(name, grid, date, time)")
    cur.close()
    con.close()

def delete_db_table():
    con = sqlite3.connect(database_location)
    cur = con.cursor()
    cur.execute("DROP TABLE results")
    cur.close()
    con.close()

def clear_table():
    try:
        delete_db_table()
    except:
        pass
    create_db_table()