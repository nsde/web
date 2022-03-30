import os
import json
import yaml
import time
import flask
import distro
import psutil
import random
import string
import threading
import jinja2.exceptions

from flask import request
from turbo_flask import Turbo
from datetime import datetime

try:
    from mcipc.query import Client
except: # server offline
    pass

from html import escape, unescape

app = flask.Flask(__name__, static_url_path='/')
app.secret_key = random.sample('ABCDEF0123456789', 6)
turbo = Turbo(app)

view_urls = {}

SERVER_NAME = 'paper'

@app.route('/x/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def template_not_found(error):
    redirects = yaml.load(open('redirects.yml'), Loader=yaml.FullLoader)
    path = error.name.replace('.html', '')

    if path in redirects.keys():
        list(flask.request.args.keys())[0] if flask.request.args.keys() else False
        return flask.redirect(redirects[path])

    return flask.render_template(f'error.html', title='Page not found!', description=f'Couldn\'t find this website: {error.name}')

@app.errorhandler(404)
def error_404(error):
    return flask.render_template(f'error.html', title='File not found!', description=f'Couldn\'t find this file.')

@app.route('/view-create', methods=['GET', 'POST'])
def create_page():
    global view_urls
    
    if request.method == 'GET':
        return flask.render_template(f'error.html', title='Unsupported request method!', description=f'This website can\'t be viewed with GET, as it\'s supposed to be POSTed.')

    code = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 5))
    view_urls[code] = request.get_json()
    

    return f'https://onlix.me/view/{code}'

def fix_formatting(text: str):
    return text.replace('  ', '&nbsp;').replace('\n', '\n<br>\n')

@app.route('/view/<code>')
def view_page(code):
    global view_urls

    if not view_urls.get(code):
        return flask.render_template(f'error.html', title='View page not found!', description=f'Couldn\'t find this code: {code}')

    return flask.render_template(f'view.html', title=fix_formatting(unescape(view_urls[code]['title'])), text=fix_formatting(unescape(view_urls[code]['text'])))

def readable_size(size):
    return round(size/1000000000, 1)

@app.route('/status')
def status_page():
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return flask.render_template(f'status.html',
        cpu=psutil.cpu_percent(),
        cpus=psutil.cpu_count(),
        threads=psutil.cpu_count(logical=False),
        ram=f'{readable_size(ram[3])}/{readable_size(ram[0])} GB ({ram[2]}%)',
        disk=f'{readable_size(disk[1])}/{readable_size(disk[0])} GB ({disk[3]}%)',

        pids=len(psutil.pids()),
        boot_days=round((time.time()-psutil.boot_time())/86400),
        os=f'{distro.linux_distribution()[0]} {distro.linux_distribution()[1]}',
    )

@app.route('/status/mc')
def status_mc():
    ops = [x['name'] for x in json.loads(open(f'/home/minecraft/{SERVER_NAME}/ops.json').read())]
    bans = [x['name'] for x in json.loads(open(f"/home/minecraft/{SERVER_NAME}/banned-players.json").read())]
    ip_bans = [x['name'] for x in json.loads(open(f"/home/minecraft/{SERVER_NAME}/banned-ips.json").read())]
    whitelist = [x['name'] for x in json.loads(open(f'/home/minecraft/{SERVER_NAME}/whitelist.json').read())]
    last_players = [x['name'] for x in json.loads(open(f'/home/minecraft/{SERVER_NAME}/usercache.json').read())[:5]]

    with Client('127.0.0.1', 25565) as client:
        server_data = client.stats(full=True)

    plugin_list = list(server_data.plugins.values())[0]

    return flask.render_template(f'status_mc.html',
        players=server_data.players,
        player_count=f'{server_data.num_players}/{server_data.max_players}' if server_data else '0/0',
        version=server_data.version if server_data else 'Offline',
        game_type=server_data.game_type if server_data else 'Server is not avaiable',
        last_player=last_players,
        last_players=len(last_players),
        whitelist=whitelist,
        whitelisted=len(whitelist),
        plugin=plugin_list,
        plugins=len(plugin_list),
        op=ops,
        ops=len(ops),
        normal_ban=bans,
        ip_ban=ip_bans,
        normal_bans=len(bans),
        ip_bans=len(ip_bans)
    )

@app.route('/red')
def red(*args, **kwargs):
    try:
        return flask.redirect(unescape(list(flask.request.args.keys())[0]))
    except IndexError:
        return flask.redirect('/')

@app.route('/mc-console-log')
def mc_console_log():
    log = []
    lines = open(f'/home/minecraft/{SERVER_NAME}/.console_history').read().split('\n')[:-1]

    for line in lines:
        line_date = line.split(':')[0]
        line_command = line.split(':')[1]
        
        for x in ['w', 'msg', 'teammsg', 'tell']:
            if line_command.startswith(x):
                line_command = f'{x} [CENSORED]'
        
        if line_command.startswith('ban-ip '):
            line_command = 'ban-ip [CENSORED IP]'
        
        if line_command.startswith('pardon-ip'):
            line_command = 'pardon-ip [CENSORED IP]'

        line_date = datetime.fromtimestamp(int(line_date)//1000).strftime('%d.%m.%y %H:%M:%S')
        
        log.append({'time': line_date, 'command': line_command})
    
    log.reverse()

    return flask.render_template(f'mcclog.html', log=log, server_name=SERVER_NAME)


def read_chat(channel=None):
    data = yaml.load(open('chats.yml'), Loader=yaml.FullLoader)
    data = data or {}
    return data.get(channel) or data

def send_message(channel, user='Guest', text=''):
    chat = read_chat()

    if not chat.get(channel):
        chat[channel] = []

    chat[channel].append({'user': user, 'text': text})
    yaml.dump(chat, open('chats.yml', 'w'), sort_keys=False, default_flow_style=False)

@app.route('/chat/<channel>', methods=['GET', 'POST'])
def chat_channel(channel):
    if flask.request.form.to_dict().get('message'):
        send_message(channel, flask.request.args.get('from') or 'Guest', flask.request.form.to_dict().get('message'))
    
    if not read_chat(channel):
        return flask.render_template(f'chat_error.html')
    return flask.render_template(f'chat.html', channel=channel, messages=reversed(read_chat(channel)))

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(flask.render_template('chat.html'), 'load'))
# @app.before_first_request
# def before_first_request():
#     threading.Thread(target=update_load).start()

# def update_load():
#     with app.app_context():
#         while True:
#             time.sleep(5)
#             turbo.push(turbo.replace(flask.render_template('chat.html'), 'load'))

### RUN CLOSED SOURCE ### 

exec(open('closed.hidden.py').read())

### ================= ###

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2021, debug=True)