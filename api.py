import blog
import tools

import os
import flask
import struct
import markupsafe

def register(app: flask.Flask):
    @app.route('/api/post')
    def api_text():
        return markupsafe.escape(flask.request.args.get('text'))

    @app.route('/api/qr/<data>')
    def api_useless(data):
        if flask.request.args.get('preview') == 'true': 
            return f'<img src="{tools.generate_qr(data)}">'
        return tools.generate_qr(data)

    @app.route('/api/blog')
    def api_blog():
        return blog.get_posts()

    @app.route('/api/blog/<post>')
    def api_blog_post(post):
        return (blog.get_info(post))
