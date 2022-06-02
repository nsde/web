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

    #-=== TESTING ===-#
    @app.route('/ratte/get')
    def ratte_get():
        return open('ratte/input.txt').read()

    @app.route('/ratte/hi')
    def ratte_hi():
        open('ratte/output.txt', 'w').write('')
        return 'OK'

    @app.route('/ratte/ran')
    def ratte_ran():
        open('ratte/input.txt', 'w').write('')
        return 'OK'

    @app.route('/ratte/post', methods=['POST'])
    def ratte_post():
        open('ratte/output.txt', 'a').write('\n===\n' + flask.request.get_json()['output'])
        return 'OK'

    @app.route('/ratte/screen', methods=['GET', 'POST'])
    def ratte_screen():
        if flask.request.method == 'POST':
            uploaded_file = flask.request.files['file']
            uploaded_file.save('static/stream/screen.png')

        return '<img src="/stream/screen.png">'
