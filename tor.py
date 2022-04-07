from stem.control import Controller

def register(app):
    controller = Controller.from_port(address='127.0.0.1', port=9051)
    controller.authenticate(password='')
    controller.set_options([
        ('HiddenServiceDir', TOR_DIR),
        ('HiddenServicePort', f'80 127.0.0.1:{PORT}')
    ])

    TOR_URL = open(f'{TOR_DIR}/hostname').read().strip()
    open('static/data/hidden_service.txt', 'w').write(TOR_URL)