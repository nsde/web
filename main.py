import blog
import tools

import os
import flask
import requests
import markupsafe

def register(app: flask.Flask, *args, **kwargs):
    DEFAULT_MODULES = ['tools', 'web']
    
    @app.route('/')
    def home():        
        return tools.render('home.html', posts=blog.get_posts()[:5])

    @app.route('/modules')
    def modules():
        modules = []
        module_count_all = 0
        module_count_active = 0

        for m in os.listdir():
            if m.endswith('.py') and not 'closed' in m:
                name = m.replace('.py', '')
                
                if name in DEFAULT_MODULES:
                    continue

                module_count_all += 1

                decs = []
                
                for line in open(m).read().split('\n'):
                    if line.strip(' \t').startswith('@app.route(\''):
                        dec = line.split('@app.route(\'')[1].split('\'')[0]

                        if not '<' in dec:
                            decs.append(dec)

                status = 'active'

                if name in tools.yml('config/disabled-modules'):
                    status = 'inactive'
                
                if name in tools.yml('data/error-modules'):
                    status = 'error'

                if status == 'active': # asking again, because a module can be "active" and "error" at the same time
                    module_count_active += 1

                modules.append({
                    'name': m,
                    'status': status,
                    'decs': decs,
                    'url': f'https://github.com/nsde/web/blob/master/{m}',
                    'error': tools.yml('data/error-modules').get(name)
                })

        return tools.render('modules.html',
            modules=modules,
            module_count_all=module_count_all,
            module_count_active=module_count_active,
            hidden_service=open('static/data/hidden_service.txt').read(),
            last_start=tools.unix_to_readable(open('logs/last_start.txt').read()),
            last_restart=tools.unix_to_readable(open('logs/last_restart.txt').read()),
        )
