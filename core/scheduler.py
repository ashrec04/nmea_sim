import asyncio
import time
from core.nmea import NEMAMessage

class Scheduler:
    def __init__(self, tick_rate_hz, sensors, loop=None):
        self.tick_time_s = 1 / tick_rate_hz
        self.sensors = sensors
        self.running = False
        self.loop = loop or asyncio.get_event_loop()

    #sim update loop runner 
    async def run(self, duration_s = None):
        self.running = True
        start_time = time.time()
        sim_tick = 0

        n2k = NEMAMessage()
        while self.running:
            now = time.time()
            for sensor in self.sensors:
                if sensor.ShouldUpdate(now):
                    reading = sensor.Update(now)
                    message = n2k.GenMessage(sensor, reading)
                    n2k.DecodeMessage(message)
            

            sim_tick += 1

            await asyncio.sleep(self.tick_time_s)
            if duration_s and ((time.time() - start_time) > duration_s):
                break