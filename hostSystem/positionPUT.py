import asyncio
import aiohttp
from ast import Pass
import numpy as np


class multiPUT:
    def __init__(self, address, prevPos):
        self.address = address
        self.prevSentPos = prevPos
    # generates task list of put requests for the asyc function

    def get_tasks(self, session):
        tasks = []
        for i in range(0, 3):
            tasks.append(session.put(self.address + 'agents/' + str(i+1), data=self.data[i]))
        return tasks

    # async function that sends the data to the server

    async def put_data(self, address):
        # put the data in r1, r2, and r3 into the server
        async with aiohttp.ClientSession() as session:
            tasks = self.get_tasks(session, address)
            try:
                await asyncio.gather(*tasks)
            except:
                Pass
    # calls the async function

    def runPut(self, pos):
        # threshold on difference in positions to stop excess put requests (the 3cm/0.03rad is just above the noise level)
        if (np.absolute(pos - self.prevSentPos) > 0.02).any():
            self.prevSentPos = np.array(pos)
            data = [{'id': 1, 'position': pos[1]}, {'id': 2, 'position': pos[2]}, {'id': 3, 'position': pos[3]}]
            asyncio.run(self.put_data(data))
