import asyncio
import time

class Scheduler:
    def __init__(self, tick_rate_hz, sensors):
        self.tick_rate_hz = tick_rate_hz
        self.sensors = sensors
        self.running = False

    #sim update loop runner 
    async def run(self, duration_s = None):
        print("TODO")