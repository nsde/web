import tools

import os
import flask

from requests_oauthlib import OAuth2Session

def register(app: flask.Flask, *args, **kwargs):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    DISCORD_API_URL = 'https://discordapp.com/api'
    CLIENT_ID = '829409199380234259'
    CLIENT_SECRET = open('../private/data/discord_login_.secret').read()
    REDIRECT_URI = 'https://onlix.me/login'
    SCOPES = ['identify', 'email']
    TOKEN_URL = 'https://discordapp.com/api/oauth2/token'
    AUTH_URL = 'https://discordapp.com/api/oauth2/authorize'

    @app.route('/login')
    def login():
        if flask.request.args.get('code'): # OAUTH CALLBACK/REDIRECT
            discord_account = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=flask.session.get('state'), scope=SCOPES)
            token = discord_account.fetch_token(
                TOKEN_URL,
                client_secret=CLIENT_SECRET,
                authorization_response=flask.request.url,
            )
            flask.session['discord_token'] = token
            return flask.redirect('/login') # LOG IN

        else:
            if flask.session.get('discord_token'): # LOGGED IN
                discord_account = OAuth2Session(CLIENT_ID, token=flask.session['discord_token'])
                profile = discord_account.get(f'{DISCORD_API_URL}/users/@me').json()
                e = profile['email']
                return tools.render('login.html', profile=profile, email=f'{e[:2]}***@{e.split("@")[1][:2]}***.{e.split(".")[-1]}')
            
            else: # NOT LOGGED IN
                oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)
                login_url, state = oauth.authorization_url(AUTH_URL)
                flask.session['state'] = state
                return tools.render('login.html', login_with_discord=login_url)
