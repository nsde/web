import tools

import os
import yaml
import flask
import secure
import random
import jinja2

def register(app: flask.Flask, *args, **kwargs):
    app.secret_key = random.sample('ABCDEF0123456789', 6)
    secure_headers = secure.Secure()

    view_urls = {}

    @app.after_request
    def set_secure_headers(response):
        secure_headers.framework.flask(response)
        return response

    @app.errorhandler(500)
    def error_500(error):
        return '500 error'

    @app.errorhandler(404)
    def error_404(error):
        rq = flask.request
        current_path = rq.path[1:]

        redirects = tools.yml('config/redirects')
        possible_template = f'templates/{current_path}.html'
        
        if current_path in redirects.keys():
            list(flask.request.args.keys())[0] if flask.request.args.keys() else False
            return flask.redirect(redirects[current_path])
        
        template = f'{current_path}.html'

        try:
            return flask.render_template(template)
        except Exception as e:
            if template == e:
                return flask.render_template(f'error.html', title='Path or file not found!', description=f'Sorry, you probably visited an old or invalid site!')
            return flask.render_template(f'error.html', title='Problems with the template', description=f'Sorry, this isn\'t your fault! An issue occurred while trying to render the template.')
