import asyncio
from tracemalloc import start
import aiohttp
import numpy as np
import requests
import datetime
address = 'http://192.168.0.181:3000/'


def get_tasks(session, data):
    tasks = []
    for i in range(0, 3):
        tasks.append(session.put(address + 'agents/' + str(i+1), data=data[i]))
    return tasks


async def put_data(data):
    # put the data in r1, r2, and r3 into the server
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, data)
        await asyncio.gather(*tasks)
pos = np.ones((4, 3))*8
startTime = datetime.datetime.now()
data = [{'id': 1, 'position': pos[1].tolist()}, {'id': 2, 'position': pos[2].tolist()}, {'id': 3, 'position': pos[3].tolist()}]
asyncio.run(put_data(data))
end = datetime.datetime.now()
print((end - startTime).total_seconds())

startTime = datetime.datetime.now()
for i in range(1, 4):
    # puts the positions onto the server for each agent
    data = {'id': i, 'position': pos[i]}
    r = requests.put(address + 'agents/' + str(i), data=data)
end = datetime.datetime.now()
print((end - startTime).total_seconds())
