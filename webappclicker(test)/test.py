import time
import asyncio
energys = 899
async def regen_energy(energy):
    while energy != 1000:
        energy += 1
        await asyncio.sleep(0.5)
loop = asyncio.get_event_loop()
loop.run_until_complete(regen_energy(energys))
loop.close()