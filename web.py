import main, misc, chat, blog, views, advanced, closed, manager

import flask

from flask_caching import Cache

app = flask.Flask(__name__, static_url_path='/')

app.config.from_mapping({
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
})
cache = Cache(app)

for library in [main, misc, chat, blog, views, advanced, closed, manager]:
    library.register(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2021, debug=True)