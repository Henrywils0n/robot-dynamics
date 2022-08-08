from flask import jsonify
import numpy as np
import requests

address = "http://192.168.0.155:3000/allPos/1"
agentPos = np.zeros((3, 3))
data = {"id": 1, "pos": agentPos.tolist()}
# make a put request to update the position all 3 agents
req = requests.put(address, json=data)
print(req.status_code)
