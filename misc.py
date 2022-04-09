import flask    
import requests
import subprocess

def register(app: flask.Flask):
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
