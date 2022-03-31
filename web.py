import main, misc, chat, blog, views, advanced, closed, manager

import flask

app = flask.Flask(__name__, static_url_path='/')

for library in [main, misc, chat, blog, views, advanced, closed, manager]:
    library.register(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2021, debug=True)