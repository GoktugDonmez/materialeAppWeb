import sqlite3

# user operations

# get all users 

def get_users():
    conn = sqlite3.connect('db/socialdata.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT id, username FROM users')
    users = cursor.fetchall()

    cursor.close()
    conn.close()
    return users