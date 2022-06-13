import json
import numpy as np

pos = np.ones((4, 3))
json_string = json.dumps([{'id': 1, 'position': pos[1].tolist()}, {'id': 2, 'position': pos[2].tolist()}, {'id': 3, 'position': pos[3].tolist()}])
print(json_string)
