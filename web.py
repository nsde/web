from flask_qrcode import QRcode
from flask_caching import Cache

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import flask

import tools

app = flask.Flask(__name__, static_url_path='/')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000 * 1000 # 2 GB
app.config.from_mapping({
    "CACHE_TYPE": "SimpleCache",
    "DEBUG": True,
    "CACHE_DEFAULT_TIMEOUT": 300
})

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=['10000 per day', '600 per hour', '60 per minute']
)

# === FLASK LIBRARIES ===
QRcode(app)
cache = Cache(app)
# === MODULES ===

modules = tools.yml('config/modules')['active']

for module in modules:
    exec(f'import {module}')
    exec(f'{module}.register(app)')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=tools.yml('config/main')['port'], debug=True)
