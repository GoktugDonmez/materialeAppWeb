from flask import Flask, render_template,url_for, request,redirect
from datetime import date
app = Flask(__name__)

posts = [{ 'id': 1,'username': 'Giacomo', 'post_date': '2 days ago',
        'user_pic': 'user.jpg', 'post_pic': 'img1.jpg', 'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl nec ultricies ultricies, nunc nisl ultricies nunc, quis ultrici'},
         
         { 'id': 2 ,'username': 'Can', 'post_date': '1 settimana fa',
        'user_pic': 'user.jpg', 'post_pic': 'img2.jpg','text': 'Random text Use the Jinja templating engine to serve web pages (homepage and "About Us") while keeping the HTML structure separate from the data managed by the application. To this end, it is necessary t'},
          ]

devs =[{ 'dev_id': 1,'devName': 'Gok2', 'quote': 'Tayyibi sikeyim', 'devPic': 'user.jpg'},
       {'dev_id': 2,'devName': 'Sezin', 'quote': 'Romaya gider miyiz', 'devPic': 'user.jpg'}
       ]

comments = [
    {'id':0, 'postid': 1, 'rate':4, 'usrname':'Can', 'usrimg': 'user.jpg', 'comment': 'Lorem ipsum dobh sed viverraSed sapien lectus, aliquam ac ornare sed, dapibus pulvinar ligula. Ut ultrices a nibh eget el sit amet felis cursus rutrum.'}, 
    {'id':1, 'postid': 1, 'rate':3, 'usrname':'Can', 'usrimg': 'user.jpg', 'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tristique lobortis molestie. Donec laoreet iaculis nibh sed viverra. Nunc condimentum tincidunt mollis. Curabitur gravida aliquam urna, ac vulputate felis condimentum at. Sed sapien lectus, aliquam ac ornare sed, dapibus pulvinar ligula. Ut ultrices a nibh eget eleifend. Nullam eleifend metus nec erat vestibulum venenatis ornare sed orci. Donec vel sapien sit amet felis cursus rutrum.', 'img':'img3.jpg'}
]

usernames = [post['username'] for post in posts]
postIds = [post['id'] for post in posts]

@app.context_processor
def inject_usernames_and_date():
    usernames = set([post['username'] for post in posts])
    today_date = date.today().isoformat()
    return dict(usernames=usernames,todayDate=today_date,comments=comments)

@app.route("/")
def home():
    return render_template('home.html', posts=posts,)


@app.route("/about")
def about():
    return render_template('about.html', devs=devs)   

@app.route("/post/<int:post_id>")
def post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    else:
        # Handle the case where no post matches the given id
        return "Post not found", 404

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

    if post['post_date'] == '':
        app.logger.error('La data del post non può essere vuota')
        return redirect(url_for('home'))
    if post['username'] not in usernames:
        app.logger.error('Username non valido')
        return redirect(url_for('home'))
    if post['text']== '':
        app.logger.error('Il contenuto del post non può essere vuoto')
        return redirect(url_for('home'))
    


    if len(post['text']) < 30 or len(post['text']) > 200:
        app.logger.error('Il contenuto del post deve essere tra 30 e 200 caratteri')
        return redirect(url_for('home'))
    if post['post_date'] < date.today().isoformat():
        app.logger.error('La data del post non può essere nel passato')
        return redirect(url_for('home'))


    foto = request.files['post_pic']
    if foto:
        foto.save('static/' + foto.filename)

    post['post_pic'] = foto.filename
    post['id'] = len(posts) + 1
    post['user_pic'] = 'user.jpg'
    posts.append(post)
    app.logger.info('Post creato con successo', post,posts)
    
    return redirect(url_for('home'))


@app.route('/comments/new', methods=['POST'])
def new_comment():
            
    comment = request.form.to_dict()

    if 'isAnonymous' in comment and comment['isAnonymous'] == 'on':
        comment['usrname'] = '@anonymous'
        comment['usrimg'] = 'anonymous.png'
    elif comment['usrname'] not in [d['username'] for d in posts]:
        app.logger.error("Non esiste l'utente!")
        return redirect(url_for('home'))
    else:
        comment['usrimg'] = [p['user_pic'] for p in posts if p['username'] == comment['usrname']][0]
    
    if comment['comment'] == '':
        app.logger.error('Il commento non può essere vuoto!')
        return redirect(url_for('home'))
    
    comment_image = request.files['image']
    if comment_image:
        comment_image.save('static/' + comment_image.filename)
        comment['img'] = comment_image.filename
            
    comment['id'] = comments[-1]['id'] + 1
    comment['postid'] = int(comment['postid'])
    comment['rate'] = int(comment['radioOptions'])
    
    comments.append(comment)
    print('Commento creato con successo', comment, comments)
    print('ananiskim')
    return redirect(url_for('post', post_id=int(comment['postid'])))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
