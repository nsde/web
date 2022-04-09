import yaml
import flask
import qrcode
import base64

from io import BytesIO

def fix_formatting(text: str):
    return text.replace('  ', '&nbsp;').replace('\n', '\n<br>\n')

def readable_size(size):
    return round(size/1000000000, 1)

def ip(request): # PRIVACY NOTICE
    if not request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['REMOTE_ADDR']
    return request.environ['HTTP_X_FORWARDED_FOR']

def yml(path: str, edit_to=None):
    path = f'{path}.yml'

    if not edit_to:
        return yaml.safe_load(open(path))
    
    yaml.dump(chat, open(path, 'w'), sort_keys=False, default_flow_style=False, indent=4)

def generate_qr(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img_buf = BytesIO()
    qr.make_image().save(img_buf)
    img_buf.seek(0)

    img_data = img_buf.read()
    img_data = base64.b64encode(img_data)
    img_data = img_data.decode()
    return f'data:image/png;base64,{img_data}'