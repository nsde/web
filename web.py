import flask

from flask_caching import Cache

PORT = 2021
TOR_DIR = '/var/lib/tor/hidden_service/'

app = flask.Flask(__name__, static_url_path='/')

app.config.from_mapping({
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
})
cache = Cache(app)

# === MODULES ===

modules = 'main misc chat blog views gaming closed manager'

for module in modules.split():
    exec(f'import {module}')
    exec(f'{module}.register(app)')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)