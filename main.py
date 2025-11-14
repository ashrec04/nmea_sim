import asyncio
import json
import sys
import os
from PyQt6.QtWidgets import QApplication

from core.sensors import DepthSensor, Anemometer, SpeedOverGround
from core.scheduler import Scheduler
from gui.gui import MainWindow

def LoadConditions(path):
    with open(path) as f:
        return json.load(f)

async def main():

    config = LoadConditions("condition_modes/calm.json")

    conditions = os.listdir('condition_modes/')
    condition_list = []
    for cond in conditions:
        cond = cond[:-5]
        condition_list.append(cond)
    print(condition_list)
    
    sensors = [
        DepthSensor(config["sensors"]["depth"]),
        Anemometer(config["sensors"]["anemometer"]),
        SpeedOverGround(config["sensors"]["speed over ground"])
    ]
    
    app = QApplication(sys.argv)
    window = MainWindow(condition_list)
    window.show()
    app.exec()

    #code wont reach here until app window closed
    #scheduler = Scheduler(config["tick_rate_hz"], sensors)
    #await scheduler.run(duration_s=10)




if __name__ == "__main__":
    asyncio.run(main())