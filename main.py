import blog

import os
import tools
import flask
import requests
import markupsafe

def register(app: flask.Flask, *args, **kwargs):
    DEFAULT_MODULES = ['tools', 'web']
    
    @app.route('/')
    def home():        
        return flask.render_template('home.html', posts=blog.get_posts()[:5])

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

                status = 'inactive'

                if name in tools.yml('config/modules')['active']:
                    status = 'active'
                
                if name in tools.yml('data/error_modules'):
                    status = 'error'

                modules.append({
                    'name': name.title(),
                    'status': status,
                    'decs': decs,
                    'url': f'https://github.com/nsde/web/blob/master/{m}',
                    'error': tools.yml('data/error_modules').get(name)
                })

        return flask.render_template('modules.html', modules=modules)