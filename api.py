import json
import blog
import tools
import flask
import httpx

def register(app: flask.Flask):
    @app.route('/api/request')
    def api_request():
        return flask.jsonify(dict((key, value) for key, value in flask.request.__dict__.iteritems() if not callable(value) and not key.startswith('__')))

    @app.route('/api/qr/<data>')
    def api_useless(data):
        if flask.request.args.get('preview') == 'true': 
            return f'<img src="{tools.generate_qr(data)}">'
        return tools.generate_qr(data)

    @app.route('/api/blog')
    def api_blog():
        return flask.jsonify(blog.get_posts())

    @app.route('/api/blog/<post>')
    def api_blog_post(post):
        return flask.jsonify((blog.get_info(post)))
