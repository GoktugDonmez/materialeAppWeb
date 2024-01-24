import sqlite3

# post operations

def get_posts():
    conn = sqlite3.connect('db/socialdata.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT posts.id, posts.data_publication, posts.post_text, posts.post_img, users.username, users.usr_img FROM posts LEFT JOIN users ON posts.id_usr = users.id ORDER BY posts.data_publication DESC')
    posts = cursor.fetchall()

    cursor.close()
    conn.close()
    return posts

def get_post(id):
    conn = sqlite3.connect('db/socialdata.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT posts.id,posts.data_publication, posts.post_text, posts.post_img, users.username, users.usr_img FROM posts LEFT JOIN users ON posts.id_usr = users.id WHERE posts.id = ?'
    post = cursor.execute(sql, (id,)).fetchone()
    cursor.close()
    conn.close()

    return post


def add_post(post):
    conn = sqlite3.connect('db/socialdata.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    if 'post_img' in post:
        insert = 'INSERT INTO posts (data_publication, post_text, post_img, id_usr) VALUES (?, ?, ?, ?)'
        post = cursor.execute(insert, (post['data_publication'],
                                        post['post_text'], post['post_img'], post['id_usr']))
    else:
        insert = 'INSERT INTO posts (data_publication, post_text, id_usr) VALUES (?, ?, ?)'
        post = cursor.execute(insert, (post['data_publication'],
                                        post['post_text'], post['id_usr']))
        
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('error', str(e))
        conn.rollback()
    
    cursor.close()
    conn.close()
    return success