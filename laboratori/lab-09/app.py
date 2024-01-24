from flask import Flask, render_template, url_for, request,redirect
from datetime import date, datetime

import postDBinteraction, userDBinteraction, commentDBinteraction

app = Flask(__name__)

posts = [{ 'id': 1,'username': 'Giacomo', 'post_date': '2 days ago',
        'user_pic': 'user.jpg', 'post_pic': 'img1.jpg', 'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl nec ultricies ultricies, nunc nisl ultricies nunc, quis ultrici'},
         
         { 'id': 2 ,'username': 'Can', 'post_date': '1 settimana fa',
        'user_pic': 'user.jpg', 'post_pic': 'img2.jpg','text': 'Random text Use the Jinja templating engine to serve web pages (homepage and "About Us") while keeping the HTML structure separate from the data managed by the application. To this end, it is necessary t'},
          ]

devs =[{ 'dev_id': 1,'devName': 'Gok2', 'quote': 'Tayyibi sikeyim', 'devPic': 'user_img.jpg'},
       {'dev_id': 2,'devName': 'Sezin', 'quote': 'Romaya gider miyiz', 'devPic': 'user_img.jpg'}
       ]

comments = [
    {'id':0, 'postid': 1, 'rate':4, 'usrname':'Can', 'usrimg': 'user.jpg', 'comment': 'Lorem ipsum dobh sed viverraSed sapien lectus, aliquam ac ornare sed, dapibus pulvinar ligula. Ut ultrices a nibh eget el sit amet felis cursus rutrum.'}, 
    {'id':1, 'postid': 1, 'rate':3, 'usrname':'Can', 'usrimg': 'user.jpg', 'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tristique lobortis molestie. Donec laoreet iaculis nibh sed viverra. Nunc condimentum tincidunt mollis. Curabitur gravida aliquam urna, ac vulputate felis condimentum at. Sed sapien lectus, aliquam ac ornare sed, dapibus pulvinar ligula. Ut ultrices a nibh eget eleifend. Nullam eleifend metus nec erat vestibulum venenatis ornare sed orci. Donec vel sapien sit amet felis cursus rutrum.', 'img':'img3.jpg'}
]

usernames = [post['username'] for post in posts]
postIds = [post['id'] for post in posts]

###
#@app.context_processor
#def inject_usernames_and_date():
#    usernames = set([post['username'] for post in posts])
#    today_date = date.today().isoformat()
#    return dict(usernames=usernames,todayDate=today_date,comments=comments)
#
###
@app.route("/")
def home():
    posts_db = postDBinteraction.get_posts()
    users_db = userDBinteraction.get_users()
    return render_template('home.html', posts=posts_db, users=users_db)


@app.route("/about")
def about():
    return render_template('about.html', devs=devs)   

@app.route("/post/<int:post_id>")
def post(post_id):
    post_db = postDBinteraction.get_post(post_id)
    comments_db = commentDBinteraction.get_comments(post_id)
    users_db = userDBinteraction.get_users()
    return(render_template('post.html', post=post_db, comments=comments_db, users=users_db))
    
    
@app.route('/post/new', methods=['POST'])
def new_post():
    """
    Create a new post.

    This function is called when a POST request is made to the '/post/new' endpoint.
    It validates the post data and saves the post to the database.

    Returns:
        redirect: A redirect response to the 'home' endpoint.

    Raises:
        KeyError: If any required field is missing in the post data.
        ValueError: If the post data is invalid.
    """
    
    post  = request.form.to_dict()

    if post['data_publication'] == '':
        app.logger.error('La data del post non può essere vuota')
        return redirect(url_for('home'))
    if post['username'] not in usernames:
        app.logger.error('Username non valido')
        return redirect(url_for('home'))
    if post['post_text']== '':
        app.logger.error('Il contenuto del post non può essere vuoto')
        return redirect(url_for('home'))
    


    if len(post['post_text']) < 30 or len(post['post_text']) > 200:
        app.logger.error('Il contenuto del post deve essere tra 30 e 200 caratteri')
        return redirect(url_for('home'))
    if post['data_publication'] < date.today().isoformat():
        app.logger.error('La data del post non può essere nel passato')
        return redirect(url_for('home'))


    foto = request.files['post_img']
    if foto:
        foto.save('static/' + foto.filename)

    success = postDBinteraction.add_post(post)
    if not success:
        app.logger.error('Errore durante la creazione del post')
    else:
        app.logger.info('Post creato con successo')

    return redirect(url_for('home'))


@app.route('/comments/new', methods=['POST'])
def new_comment():
            
    comment = request.form.to_dict()

    if 'isAnonymous' in comment and comment['isAnonymous'] == 'on':
        comment['usr_id'] = None
    else:
        comment['usr_id'] = int(comment['usr_id'])

    if comment['text'] == '':
        app.logger.error('Il commento non può essere vuoto!')
        return redirect(url_for('home'))
    
    comment_image = request.files['comment_img']
    if comment_image:
        comment_image.save('static/' + comment_image.filename)
        comment['comment_img'] = comment_image.filename
            
    comment['post_id'] = int(comment['postid'])
    comment['rating'] = int(comment['radioOptions'])

    success = commentDBinteraction.add_comment(comment)
    if not success:
        app.logger.error('Errore durante la creazione del commento')
    else:
        app.logger.info('Commento creato con successo')

    return redirect(url_for('post', post_id=comment['post_id']))




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
