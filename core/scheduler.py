import asyncio
import time
from core.nmea import NEMAMessage

class Scheduler:
    def __init__(self, tick_rate_hz, sensors, loop=None):
        self.tick_time_s = 1 / tick_rate_hz
        self.sensors = sensors
        self.running = False
        self.sim_started = False
        self.loop = loop or asyncio.get_event_loop()

    def SetRun(self):
        if not self.sim_started:
            self.sim_started = True
            self.running = True
    #initise run
    async def Run(self, duration_s = None):
        self.SetRun()
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
    
    async def Stop(self):
        self.running = False
        self.sim_started = False