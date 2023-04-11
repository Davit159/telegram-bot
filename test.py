import requests

x = requests.get('https://localhost.com')
print(x.status_code)