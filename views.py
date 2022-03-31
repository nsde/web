import tools

import flask
import random
import string

def register(app: flask.Flask):
    @app.route('/view-create', methods=['GET', 'POST'])
    def create_page():
        global view_urls
        
        if flask.request.method == 'GET':
            return flask.render_template(f'error.html', title='Unsupported request method!', description=f'This website can\'t be viewed with GET, as it\'s supposed to be POSTed.')

        code = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 5))
        view_urls[code] = request.get_json()
        

        return f'https://onlix.me/view/{code}'

    @app.route('/view/<code>')
    def view_page(code):
        global view_urls

        if not view_urls.get(code):
            return flask.render_template(f'error.html', title='View page not found!', description=f'Couldn\'t find this code: {code}')

        return flask.render_template(f'view.html', title=tools.fix_formatting(unescape(view_urls[code]['title'])), text=tools.fix_formatting(unescape(view_urls[code]['text'])))