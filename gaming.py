MINECRAFT_SERVER_NAME = 'purpur'

import tools

import json
import time
import flask
import psutil
import distro

try:
    from mcipc.query import Client
except: # server offline
    pass

def register(app: flask.Flask):
    @app.route('/status/mc')
    def status_mc():
        ops = [x['name'] for x in json.loads(open(f'/home/minecraft/{MINECRAFT_SERVER_NAME}/ops.json').read())]
        bans = [x['name'] for x in json.loads(open(f"/home/minecraft/{MINECRAFT_SERVER_NAME}/banned-players.json").read())]
        ip_bans = [x['name'] for x in json.loads(open(f"/home/minecraft/{MINECRAFT_SERVER_NAME}/banned-ips.json").read())]
        whitelist = [x['name'] for x in json.loads(open(f'/home/minecraft/{MINECRAFT_SERVER_NAME}/whitelist.json').read())]
        last_players = [x['name'] for x in json.loads(open(f'/home/minecraft/{MINECRAFT_SERVER_NAME}/usercache.json').read())[:5]]

        try:
            with Client('127.0.0.1', 25565) as client:
                server_data = client.stats(full=True)
        except:
            return flask.render_template('error.html', title='Minecraft Server Offline', description='Sorry, you can\'t view this Minecraft server\'s stats, because it\'s offline (or starting)!')

        plugin_list = []

        if server_data.plugins:
            plugin_list = list(server_data.plugins.values())[0]

        return flask.render_template('status_mc.html',
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

    @app.route('/status')
    def status_page():
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return flask.render_template(f'status.html',
            cpu=psutil.cpu_percent(),
            cpus=psutil.cpu_count(),
            threads=psutil.cpu_count(logical=False),
            ram=f'{tools.readable_size(ram[3])}/{tools.readable_size(ram[0])} GB ({ram[2]}%)',
            disk=f'{tools.readable_size(disk[1])}/{tools.readable_size(disk[0])} GB ({disk[3]}%)',

            pids=len(psutil.pids()),
            boot_days=round((time.time()-psutil.boot_time())/86400),
            os=f'{distro.linux_distribution()[0]} {distro.linux_distribution()[1]}',
        )

    @app.route('/mc-console-log')
    def mc_console_log():
        log = []
        lines = open(f'/home/minecraft/{MINECRAFT_SERVER_NAME}/.console_history').read().split('\n')[:-1]

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

        return flask.render_template(f'mcclog.html', log=log, server_name=MINECRAFT_SERVER_NAME)
