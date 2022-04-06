import blog

import os
import flask
import requests

def register(app: flask.Flask):
    @app.route('/')
    def home():        
        return flask.render_template('home.html', posts=blog.get_posts()[:5])

    @app.route('/red')
    def red(*args, **kwargs):
        try:
            return flask.redirect(unescape(list(flask.request.args.keys())[0]))
        except IndexError:
            return flask.redirect('/')
