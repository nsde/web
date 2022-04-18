import tools

import os
import flask    
import requests
import subprocess

from werkzeug.utils import secure_filename

def register(app: flask.Flask):
    @app.route('/share', methods=['GET', 'POST'])
    def share_upload():
        if flask.request.method == 'POST':
            if 'file' not in flask.request.files:
                return flask.render_template('error.html', title='No file found!', description='No file was submitted correctly. Please try again.')

            uploaded_file = flask.request.files['file']

            if uploaded_file.filename == '':
                return flask.render_template('error.html', title='No file found!', description='No file was submitted correctly. Please try again.')

            if uploaded_file:
                filename = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join('share', filename))
               
                link = f'https://onlix.me/share/{filename}'
                return flask.render_template('uploaded.html', name=filename, qr=tools.generate_qr(link), link=link)            

        return flask.render_template('share.html')

    @app.route('/share/<name>')
    def share_download(name):
        return flask.send_file(f'share/{name}')

    @app.route('/reload/lila.css')
    def lilacss_cdn():
        error = 'Unknown'

        try:
            css_code = requests.get('https://raw.githubusercontent.com/nsde/lilacss/main/lila.css').text
        except Exception as e:
            error = e

        bg_code = '{background-color: black;}'
        bsn = '\n'

        if css_code:
            open('static/style/lila.css', 'w').write(css_code) 

            return f'''<style>*{bg_code}</style><h1 style="color: lightgreen;">Success, added {open("static/style/lila.css").read().count(bsn)-css_code.count(bsn)} lines</h1>'''            
        else:
            return f'''<style>*{bg_code}</style><h1 style="color: red;">Error {error}</h1>'''
