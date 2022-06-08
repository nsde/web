import tools

import os
import flask
import getpass

from requests_oauthlib import OAuth2Session

def register(app: flask.Flask, *args, **kwargs):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    DISCORD_API_URL = 'https://discordapp.com/api'
    CLIENT_ID = '829409199380234259'
    CLIENT_SECRET = getpass.getpass()
    REDIRECT_URI = 'https://example.com:8000/oauth_callback'
    SCOPES = ['identify', 'email']
    TOKEN_URL = 'https://discordapp.com/api/oauth2/token'
    AUTH_URL = 'https://discordapp.com/api/oauth2/authorize'

    @app.route('/login')
    def login():
        return 'hi!'
        if flask.request.args.get('code'): # OAUTH CALLBACK/REDIRECT
            discord_account = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=session['state'], scope=SCOPES)
            token = discord_account.fetch_token(
                TOKEN_URL,
                client_secret=client_secret,
                authorization_response=flask.request.url,
            )
            flask.session['discord_token'] = token
            flask.redirect('/login')

        else:
            if session['discord_token']: # LOGGED IN
                discord_account = OAuth2Session(client_id, token=session['discord_token'])
                profile = discord_account.get(f'{DISCORD_API_URL}/users/@me').json()
                return tools.render('login.html', profile=profile)
            
            else: # NOT LOGGED IN
                oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)
                login_url, state = oauth.authorization_url(AUTH_URL)
                session['state'] = state
                return login_url
                return tools.render('login.html', login_with_discord=login_url)
