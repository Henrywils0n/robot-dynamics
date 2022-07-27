import requests
from sympy import re

address = 'http://127.0.0.1:5000/agents/1'

req = requests.get(address)
print(req.text)

req = requests.put(address, json={'id': 1, 'position': [1, 2, 3]})
