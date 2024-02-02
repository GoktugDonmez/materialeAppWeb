from flask import Flask, render_template, url_for, request,redirect
from datetime import date, datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from model import User
import postDBinteraction, userDBinteraction, commentDBinteraction

# Configuration for the Flask-Login extension

app = Flask(__name__)

app.config['SECRET_KEY'] =  'some value' # TODO: Change this!

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """
    This function is used by Flask-Login to load a User object from the database given its id.
    """
    db_user = userDBinteraction.get_user(user_id)
    user = User(db_user['id'], db_user['username'], db_user['password'],
                 db_user['profile_pic'])

    return user


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
    devs =[{ 'dev_id': 1,'devName': 'Gok2', 'quote': 'Tayyibi sikeyim', 'devPic': 'user_img.jpg'},
       {'dev_id': 2,'devName': 'Sezin', 'quote': 'Romaya gider miyiz', 'devPic': 'user_img.jpg'}
       ]

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
