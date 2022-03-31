import tools

import flask
import subprocess

def register(app: flask.Flask):
    @app.route(f'/{open("../private/data/admin_code.txt").read()}/<cmd>')
    def admin_command(cmd):
        if tools.ip(flask.request) not in open("../private/data/admin_ips.txt").read():
            return flask.abort(403)
        
        try:
            output = subprocess.check_output(f'echo q | {cmd} | aha --black --line-fix', shell=True).decode('utf-8')
        except Exception as e:
            output = str(e)

        output = f'<h1><code>{cmd}</code></h1>\n{output}'

        return output