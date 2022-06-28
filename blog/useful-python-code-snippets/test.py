import requests
import webbrowser

response = requests.get('https://ipinfo.io/json').json()
print(response['ip'])
print(f'{response["city"]} in {response["region"]}, {response["country"]}')
print(response.get('org') or 'No organization.')

if response.get('hostname'): # website detected on server
    if input(f'Website detected: {response.get("hostname")}. Type y and press enter to open.') == 'y':
        webbrowser.open('hostname')
