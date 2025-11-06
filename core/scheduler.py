import asyncio
import time

class Scheduler:
    def __init__(self, tick_rate_hz, sensors):
        self.tick_time_s = 1 / tick_rate_hz
        self.sensors = sensors
        self.running = False

    #sim update loop runner 
    async def run(self, duration_s = None):
        self.running = True
        start_time = time.time()
        sim_tick = 0

        while self.running:
            now = time.time()
            for sensor in self.sensors:
                if sensor.ShouldUpdate(now):
                    reading = sensor.Update(now)
                    print(sensor.name, " : ", reading)
            

            sim_tick += 1

            await asyncio.sleep(self.tick_time_s)
            if duration_s and ((time.time() - start_time) > duration_s):
                break