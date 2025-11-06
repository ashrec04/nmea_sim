import asyncio
import json

from core.sensors import DepthSensor, Anemometer, SpeedOverGround
from core.scheduler import Scheduler

def LoadConditions(path):
    with open(path) as f:
        return json.load(f)

async def main():

    config = LoadConditions("condition_modes/calm.json")
    
    sensors = [
        DepthSensor(config["sensors"]["depth"]),
        Anemometer(config["sensors"]["anemometer"]),
        SpeedOverGround(config["sensors"]["speed over ground"])
    ]

    scheduler = Scheduler(config["tick_rate_hz"], sensors)
    await scheduler.run(duration_s=10)


if __name__ == "__main__":
    asyncio.run(main())