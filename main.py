import blog

import flask

def register(app: flask.Flask):
    @app.route('/')
    def home():        
        return flask.render_template('home.html', posts=blog.get_posts()[:5])