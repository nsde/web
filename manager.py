import os
import yaml
import flask
import secure
import random
import jinja2

from turbo_flask import Turbo

def register(app: flask.Flask):
    app.secret_key = random.sample('ABCDEF0123456789', 6)
    secure_headers = secure.Secure()
    turbo = Turbo(app)

    view_urls = {}

    @app.after_request
    def set_secure_headers(response):
        secure_headers.framework.flask(response)
        return response

    @app.errorhandler(jinja2.exceptions.TemplateNotFound)
    def template_not_found(error):
        path = error.name.replace('.html', '')

        return flask.render_template(f'error.html', title='Page not found!', description=f'Couldn\'t find this website: {error.name}')

    @app.errorhandler(404)
    def error_404(error):
        rq = flask.request
        current_path = rq.path[1:]

        redirects = yaml.load(open('redirects.yml'), Loader=yaml.FullLoader)
        possible_template = f'templates/{current_path}.html'
        if current_path in redirects.keys():
            list(flask.request.args.keys())[0] if flask.request.args.keys() else False
            return flask.redirect(redirects[current_path])
            
        try:
            return flask.render_template(f'{current_path}.html')
        except:
            return flask.render_template(f'error.html', title='File not found!', description=f'Couldn\'t find this file.')

    # @app.before_first_request
    # def before_first_request():
    #     threading.Thread(target=update_load).start()

    # def update_load():
    #     with app.app_context():
    #         while True:
    #             time.sleep(5)
    #             turbo.push(turbo.replace(flask.render_template('chat.html'), 'load'))

    # @app.before_first_request
    # def before_first_request():
    #     threading.Thread(target=update_load).start()

    # def update_load():
    #     with app.app_context():
    #         while True:
    #             time.sleep(5)
    #             turbo.push(turbo.replace(flask.render_template('chat.html'), 'load'))
