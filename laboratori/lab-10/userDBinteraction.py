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

def get_user(user_id):
    conn = sqlite3.connect('db/socialdata.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT id, username, password, profile_pic FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user