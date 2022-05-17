import tools

import os
import flask
import random
import requests
import subprocess

from werkzeug.utils import secure_filename

def register(app: flask.Flask):
    @app.route('/personify')
    def personify():
        return flask.render_template('personify.html', p=requests.get('https://random-data-api.com/api/users/random_user').json())

    @app.route('/bored')
    def bored():
        no = '''
No, that's boring, too.
No...
Another one...
Nope...
No?!
Sorry, no...
I don't want to do this..!
Another one, please!
Next one!
Another one!
Generate one more!
Gimme another one, please!
Boorinng!
Can you show me another one, please?
Show me another activity, please!
'''        
        return flask.render_template('bored.html', data=requests.get('https://www.boredapi.com/api/activity').json(), no=random.choice(no.split('\n')))

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
