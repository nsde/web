import flask

def register(app: flask.Flask, cache, *args, **kwargs):
    @app.after_request
    def add_cors_headers(response):
        if flask.request.path.startswith('/cdn/'):
            add_header = response.headers.add

            add_header('Access-Control-Allow-Origin', '*')
            add_header('Access-Control-Allow-Credentials', 'true')
            add_header('Access-Control-Allow-Headers', 'Content-Type')
            add_header('Access-Control-Allow-Headers', 'Cache-Control')
            add_header('Access-Control-Allow-Headers', 'X-Requested-With')
            add_header('Access-Control-Allow-Headers', 'Authorization')
            add_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        
        return response
