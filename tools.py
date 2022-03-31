import flask

def fix_formatting(text: str):
    return text.replace('  ', '&nbsp;').replace('\n', '\n<br>\n')

def readable_size(size):
    return round(size/1000000000, 1)

def ip(request):
    if not request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['REMOTE_ADDR']
    return request.environ['HTTP_X_FORWARDED_FOR']