import tools
import flask
import markdown
import markupsafe

from datetime import datetime

def register(app: flask.Flask, *args, **kwargs):
    @app.route('/novaport')
    def novaport():
        return flask.render_template('novaport-upload.html')

    @app.route('/novaport/<code>', defaults={'channel': ':'})
    @app.route('/novaport/<code>/<channel>')
    def novaport_code(code, channel):
        if code == 'upload':
            code = flask.request.args.get('code')
            if '/view/' in code:
                code = code.split('/view/')[0]

        try:
            export = tools.yml(f'data/views/{code}').get(code)

            if not export:
                raise Exception('View not found')
        except Exception as e:
            return flask.render_template('novaport-upload.html', error=str(e))

        if channel == ':':
            channel = list(export.keys())[0]
            channel_data = list(export.values())[0]
        else:
            channel_data = export[channel]

        messages = []
        for message in channel_data:
            messages.append({
                'author': message['author'],
                'time': datetime.utcfromtimestamp(message['timestamp']).strftime('%Y/%m/%d %H:%M'),
                'html': markdown.markdown(markupsafe.escape(message['text'])).replace('<p>', '').replace('</p>', ''),
            })

        return flask.render_template('novaport.html',
            export_code=code,
            current_channel=channel,
            channel_list=list(export.keys()),
            messages=messages,
        )