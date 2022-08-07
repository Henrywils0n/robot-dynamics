from flask import jsonify
import numpy as np
import requests

address = "http://192.168.0.181:3000/agents?id=1,2,3"
agentPos = np.zeros((3, 3))
data = [{"id": 1, "position": agentPos[0, :]}, {"id": 2, "position": agentPos[1, :]}, {"id": 3, "position": agentPos[2, :]}]
# make a put request to update the position all 3 agents
req = requests.put(address, data=data)
