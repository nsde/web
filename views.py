import tools

import flask
import random
import requests
import markupsafe

def register(app: flask.Flask, *args, **kwargs):
    @app.route('/view/new', methods=['GET', 'POST'])
    def view_create():
        if flask.request.method == 'GET':
            return tools.render(f'error.html', title='Unsupported request method!', description=f'This website can\'t be viewed with GET, as it\'s supposed to be POSTed.')

        code = requests.get('https://random-word-api.herokuapp.com/word').json()[0] + str(random.randint(1, 9))
        views = tools.yml(f'data/views/{code}')
        data = flask.request.get_json()
        
        if not isinstance(views, dict):
            views = {}
        views[code] = data

        tools.yml(f'data/views/{code}', edit_to=views)

        return f'https://onlix.me/view/{code}'

    @app.route('/view/<code>')
    def view_page(code):
        view = tools.yml(f'data/views/{code}').get(code)

        if not view:
            return tools.render(f'error.html', title='View page not found!', description=f'Couldn\'t find this code: {code}')

        return flask.jsonify(view)

