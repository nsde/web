from flask_qrcode import QRcode
from flask_caching import Cache

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

import flask

import tools

app = flask.Flask(__name__, static_url_path='/')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000 * 1000 # 1 GB
app.config.from_mapping({
    "CACHE_TYPE": "SimpleCache",
    "DEBUG": True,
    "CACHE_DEFAULT_TIMEOUT": 300
})
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

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

tools.yml('data/error_modules', {})

for module in modules:
    try:
        exec(f'import {module}')
        exec(f'{module}.register(app)')
    except Exception as e:
        print(f'[ERROR] {module}: {e}')
        
        error_yml = tools.yml('data/error_modules')
        error_yml[module] = str(e)
        tools.yml('data/error_modules', error_yml)

@app.before_request
def block_method():
    if tools.ip(flask.request) in tools.yml('config/banned-ips'):
        flask.abort(403, 'IP Ban (because of spamming/DDoS) suspect.')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=tools.yml('config/main')['port'], debug=True)
