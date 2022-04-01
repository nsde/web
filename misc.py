import flask    
import requests
import subprocess

def register(app: flask.Flask):
    @app.route('/dbd')
    def dbd():
        posts = subprocess.check_output(f'twint -u dbdcodes', shell=True).decode('utf-8')
        scraped_posts = []

        for post in posts.split('\n')[:-3]:
            print(post)
            post_time = ' '.join(post.split()[1:3])
            post_text = post.split('> ')[1].split(' https://t.co/')[0]
            post_url = post.split()[-1]
            
            post_blood = 0
            post_shards = 0

            if 'k Bloodpoints' in post_text:
                post_blood = int(post_text.split(' For ')[1].split('k Bloodpoints')[0])

            if ',000 Bloodpoints' in post_text:
                post_blood = int(post_text.split(' For ')[1].split(',000 Bloodpoints')[0])

            if ' Iridescent Shards' in post_text:
                post_shards = int(post_text.split(' Iridescent Shards')[0].split()[-1].replace('k', '000'))
            
            detected = (not (post_blood or post_shards))

            if not post_text.startswith('@'):
                scraped_posts.append({
                    'time': post_time,
                    'text': post_text,
                    'url': post_url,
                    
                    'blood': '♦️'*(post_blood//25) or ' ',
                    'shards': '💠'*(post_shards//170) or ' ',
                    
                    'style': 'color: gray;' if detected else '',
                    'detected': 'ℹ️' if detected else ''
                })

        return flask.render_template('dbd.html', posts=scraped_posts)

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
            open('static/lila.css', 'w').write(css_code) 

            return f'''<style>*{bg_code}</style><h1 style="color: lightgreen;">Success, added {open("static/lila.css").read().count(bsn)-css_code.count(bsn)} lines</h1>'''            
        else:
            return f'''<style>*{bg_code}</style><h1 style="color: red;">Error {error}</h1>'''
