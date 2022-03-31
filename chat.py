import flask

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


def register(app: flask.Flask):
    @app.route('/chat/<channel>', methods=['GET', 'POST'])
    def chat_channel(channel):
        if flask.request.form.to_dict().get('message'):
            send_message(channel, flask.request.args.get('from') or 'Guest', flask.request.form.to_dict().get('message'))
        
        if not read_chat(channel):
            return flask.render_template(f'chat_error.html')
        return flask.render_template(f'chat.html', channel=channel, messages=reversed(read_chat(channel)))
