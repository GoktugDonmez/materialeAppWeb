from flask import Flask, render_template,url_for


app = Flask(__name__)

posts = [{ 'id': 31,'username': 'Giacomo', 'post_date': '2 days ago',
        'user_pic': 'user.jpg', 'post_pic': 'img1.jpg', 'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl nec ultricies ultricies, nunc nisl ultricies nunc, quis ultrici'},
         
         { 'id': 32 ,'username': 'Can', 'post_date': '1 settimana fa',
        'user_pic': 'user.jpg', 'post_pic': 'img2.jpg','text': 'Random text Use the Jinja templating engine to serve web pages (homepage and "About Us") while keeping the HTML structure separate from the data managed by the application. To this end, it is necessary t'},
          ]

devs =[{ 'dev_id': 1,'devName': 'Gok2', 'quote': 'Tayyibi sikeyim', 'devPic': 'user.jpg'},
       {'dev_id': 2,'devName': 'Sezin', 'quote': 'Romaya gider miyiz', 'devPic': 'user.jpg'}
       ]



@app.route("/")
def index():
    return render_template('index.html', posts=posts) 

@app.route("/about")
def about():
    return render_template('about.html', devs=devs)

