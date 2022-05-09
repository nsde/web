import blog

import os
import tools
import flask

def register(app: flask.Flask):
    DEFAULT_MODULES = ['tools', 'web']
    
    @app.route('/')
    def home():        
        return flask.render_template('home.html', posts=blog.get_posts()[:5])

    @app.route('/en')
    def home_en():
        return flask.redirect('/')

    @app.route('/modules')
    def modules():
        modules = []

        for m in os.listdir():
            if m.endswith('.py') and not 'closed' in m:
                name = m.replace('.py', '')
                
                if name in DEFAULT_MODULES:
                    continue

                decs = []
                
                for line in open(m).read().split('\n'):
                    if line.strip(' \t').startswith('@app.route(\''):
                        dec = line.split('@app.route(\'')[1].split('\'')[0]

                        if not '<' in dec:
                            decs.append(dec)

                modules.append({
                    'name': name.title(),
                    'status': name in tools.yml('config/modules')['active'],
                    'decs': decs,
                    'url': f'https://github.com/nsde/web/blob/master/{m}'
                })

        return flask.render_template('modules.html', modules=modules)