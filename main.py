import blog

import os
import flask
import requests

def register(app: flask.Flask):
    @app.route('/')
    def home():        
        return flask.render_template('home.html', posts=blog.get_posts()[:5])