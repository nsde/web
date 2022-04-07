import yaml
import flask

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