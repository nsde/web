MINECRAFT_SERVER_NAME = 'purpur'

import tools

import json
import time
import flask
import psutil
import distro
import requests
import subprocess

try:
    from mcipc.query import Client
except: # server offline
    pass

def register(app: flask.Flask, *args, **kwargs):
    @app.route('/shopcraft')
    def shopcraft():
        return tools.render('mc-shop.html', articles=[
            {
                'image': 'https://imgs.search.brave.com/PVJIp0wz0OfZVeyZuQEIs7fVtZN1qd9z9xvdciIJu8M/rs:fit:160:160:1/g:ce/aHR0cDovL2ltZzMu/d2lraWEubm9jb29r/aWUubmV0L19fY2Iy/MDEyMTExMDE5MDEx/NC9taW5lY3JhZnQv/aW1hZ2VzLzgvOGYv/R2hhc3RfVGVhci5w/bmc',
                'price': '4',
                'title': '1x Ghast Träne',
                'description': 'Egal ob du sie für Regenerations-Tränke (zum Heilen) oder Enderkristalle (welche sehr OP für PvP sind) brauchst, Ghasttränen sind ein ziemlich wertvolles Gut.'
            },
            {
                'image': '/images/minecraft/shulker_shell.webp',
                'price': '2',
                'title': '2x Shulker Schalen',
                'description': 'Shulker kann man nie genug haben - unabhängig davon, ob für einen Shop, ein Lager oder deine Endertruhe. '
            },
            {
                'image': '/images/minecraft/chest.webp',
                'price': 'GRATIS',
                'title': '1x Truhe',
                'description': 'Gratis je Kauf von 2 Shulkerschalen! Das heißt, du kannst deine Shulkerschalen sofort umcraften.',
                'special': True
            }
        ])

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
            return tools.render('error.html', title='Minecraft Server Offline', description='Sorry, you can\'t view this Minecraft server\'s stats, because it\'s offline (or starting)!')

        plugin_list = []

        if server_data.plugins:
            plugin_list = list(server_data.plugins.values())[0]

        return tools.render('status_mc.html',
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

        return tools.render('status.html',
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

        return tools.render('mcclog.html', log=log, server_name=MINECRAFT_SERVER_NAME)

    @app.route('/dbd')
    def dbd():
        posts = subprocess.check_output(f'twint -u dbdcodes', shell=True).decode('utf-8')
        scraped_posts = []

        for post in posts.split('\n')[:-3]:
            post_time = ' '.join(post.split()[1:3])
            post_text = post.split('> ')[1].split(' https://t.co/')[0]
            post_url = post.split()[-1]
            
            post_blood = 0
            post_shards = 0

            if 'k Bloodpoints' in post_text:
                post_blood = int(post_text.split(' For ')[1].split('k Bloodpoints')[0])

            if ',000 Bloodpoints' in post_text:
                post_blood = int(post_text.split(' For ')[1].split(',000 Bloodpoints')[0])

            if ' Iridescent Shards' in post_text:
                post_shards = int(post_text.split(' Iridescent Shards')[0].split()[-1].replace('k', '000'))
            
            detected = (not (post_blood or post_shards))

            if not post_text.startswith('@'):
                scraped_posts.append({
                    'time': post_time,
                    'text': post_text,
                    'url': post_url,
                    
                    'blood': '♦️'*(post_blood//25) or ' ',
                    'shards': '💠'*(post_shards//170) or ' ',
                    
                    'style': 'color: gray;' if detected else '',
                    'detected': 'ℹ️' if detected else ''
                })

        return tools.render('dbd.html', posts=scraped_posts)
