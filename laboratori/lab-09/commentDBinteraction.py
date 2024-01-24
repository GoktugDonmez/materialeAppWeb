import sqlite3

# get comments for a post

def get_comments(post_id):
    conn = sqlite3.connect('db/socialdata.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT comments.id, comments.data_publication, comments.text, users.username, users.usr_img, comments.post_id FROM comments LEFT JOIN users ON comments.usr_id = users.id WHERE comments.post_id = ?'
    cursor.execute(sql, (post_id,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()
    return comments

# add a comment to a post
def add_comment(comment):
    conn = sqlite3.connect('db/socialdata.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()


    sql = 'INSERT INTO comments (data_publication, comment_text, id_usr, id_post, comment_img) VALUES (?, ?, ?, ?, ?)'
    cursor.execute(sql, (comment['data_publication'], comment['comment_text'], comment['id_usr'],
                          comment['id_post'], comment['comment_img']))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('error', str(e))
        conn.rollback()
        success = False 
    
    cursor.close()
    conn.close()
    return success
