import blog

import os
import flask
import requests

def register(app: flask.Flask):
    @app.route('/')
    def home():
        # status_data = requests.get('https://discord.com/api/guilds/717380468923695186/widget.json').json()
        
        # try:
        #     my_status = [m for m in status_data['members'] if m['username'] == 'ONLIX'][0]
        # except:
        #     my_status = None
        # repos=requests.get('https://api.github.com/users/nsde/repos').json()
        
        return flask.render_template('home.html', posts=blog.get_posts()[:3])

    @app.route('/red')
    def red(*args, **kwargs):
        try:
            return flask.redirect(unescape(list(flask.request.args.keys())[0]))
        except IndexError:
            return flask.redirect('/')
