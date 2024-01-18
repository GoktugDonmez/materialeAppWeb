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

usernames = [post['username'] for post in posts]


@app.context_processor
def inject_usernames_and_date():
    usernames = set([post['username'] for post in posts])
    today_date = date.today().isoformat()
    return dict(usernames=usernames,todayDate=today_date)

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



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)