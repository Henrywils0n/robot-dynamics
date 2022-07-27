import requests
address = 'http://127.0.0.1:5000/agentReady'

req = requests.get(address)
print(req.text)
