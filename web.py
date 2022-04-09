import tools

import flask

from flask_qrcode import QRcode
from flask_caching import Cache

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = flask.Flask(__name__, static_url_path='/')

app.config.from_mapping({
    "CACHE_TYPE": "SimpleCache",
    "DEBUG": True,
    "CACHE_DEFAULT_TIMEOUT": 300
})

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=['10000 per day', '600 per hour', '30 per minute']
)

# === FLASK LIBRARIES ===
QRcode(app)
cache = Cache(app)
# === MODULES ===

modules = 'main misc chat blog views gaming closed manager tor'

for module in modules.split():
    exec(f'import {module}')
    exec(f'{module}.register(app)')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=tools.yml('config/main')['port'], debug=True)