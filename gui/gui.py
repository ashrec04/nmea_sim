import asyncio
import json
import ctypes
from collections import deque
from qasync import asyncSlot
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QLabel, QScrollArea, QButtonGroup
from PyQt6 import uic

from core.sensors import DepthSensor, Anemometer, VesselSpeed, BilgeStatus, EngineStatus
from core.scheduler import Scheduler

'''GUI System 
    - Calles the schedules
    - Controls which sensors and conditions are chosen
'''

#~~ Global Constants
APPLICATION_NAME = "NMEA 2000 Sim"
ICON_PATH = 'gui/resources/icon.ico'
WINDOW_PATH = 'gui/resources/mainwindow.ui'
#~~

# Subclass QMainWindow to customise the window
class MainWindow(QMainWindow):

    def __init__(self, condition_list, loop=None):
        super().__init__()

        uic.loadUi(WINDOW_PATH, self)   # loads window as defined in mainwindow.ui

        # setup app window and icon
        self.setWindowTitle(APPLICATION_NAME)
        # self.setFixedSize(self.size())
        self.setWindowIcon(QIcon(ICON_PATH))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('nmea-sim.gui')

        # wire up widgets from .ui
        self.modeListWidget.addItems(condition_list)
        self.modeListWidget.currentItemChanged.connect(self.ModeChosen)
        self.errorLabel.setText("")
        self.startButton.clicked.connect(self.PlayButtonClicked)     # start
        self.stopButton.clicked.connect(self.StopButtonClicked)   # stop


        # bilge level slider to label and save value
        self.bilge_level = 0
        self.bilgeLevelSlider.setRange(0, 100)
        self.bilgeLevelSlider.setValue(self.bilge_level)
        self.levelPercentlabel.setText(f"{self.bilge_level}%")
        self.bilgeLevelSlider.valueChanged.connect(self.OnBilgeLevelChanged)


        # on/off engine radio button grouping
        self.engine_status = 1200 # on = 1200 off = 0 (rpm)
        self.engine_stat_changed_callback = None

        self.engine_group = QButtonGroup(self)
        self.engine_group.setExclusive(True)
        self.engine_group.addButton(self.engOnRadioButton)
        self.engine_group.addButton(self.engOffRadioButton)

        self.engOnRadioButton.toggled.connect(self.UpdateEngineStatus)
        self.engOnRadioButton.setChecked(self.engine_status)
        self.engOffRadioButton.setChecked(not self.engine_status)


        # log label lives inside the scroll area
        self.log_label: QLabel = self.findChild(QLabel, "logLabel")
        self.log_label.setText("")  # start empty
        self.log_entries = deque(maxlen=150)  # keep only the most recent 150 logs


        self.mode_chosen = None
        self.sim_running = False
        self.loop = loop or asyncio.get_event_loop()
        self.log_queue = asyncio.Queue()
        self.loop.create_task(self.UpdateLogLabel())
        self.scheduler = None


    def ModeChosen(self, m):
        self.mode_chosen = m.text()


    @asyncSlot()
    async def PlayButtonClicked(self):
        if self.sim_running == True:
            return
        else:
            try:
                config = LoadConditions(self.mode_chosen)
                self.UpdateErrorLabel(f"Transmitting sensor data for\n{self.mode_chosen} conditions")
            except:
                self.UpdateErrorLabel("Start Invalid:\n\nYou must choose a condition\nto start the simulation")

            
            sensors = [
                DepthSensor(config["sensors"]["depth"]),
                Anemometer(config["sensors"]["anemometer"]),
                VesselSpeed(config["sensors"]["vessel speed"]),
                BilgeStatus(lambda: self.bilge_level),
                EngineStatus(lambda: self.engine_status)
            ]

            self.scheduler = Scheduler(config["tick_rate_hz"], sensors, self.loop, self.log_queue)
            try:
                self.ResetLogLabel()
                self.sim_running = True
                await self.scheduler.Run()
                
            except Exception as e:
                self.sim_running = False
                self.UpdateErrorLabel("ERROR: scheduler has encountered an issue\n:", e)
            
    @asyncSlot()
    async def StopButtonClicked(self):
        if self.sim_running == True:
            await self.scheduler.Stop()
            self.sim_running = False
            self.UpdateErrorLabel("Simulation Stopped")
        else:
            self.sim_running = False

    async def UpdateLogLabel(self):
        while True:
            message = await self.log_queue.get()
            self.log_entries.append(message)
            self.log_label.setText("\n".join(self.log_entries))
            self.log_label.adjustSize()  # let label report its new height
            self.log_label.parent().adjustSize()  # keep scroll widget in sync
            
            self.scrollArea.verticalScrollBar().setValue(
                self.scrollArea.verticalScrollBar().maximum()
            )
            
            self.log_queue.task_done()

    def ResetLogLabel(self):
        self.log_entries.clear()
        self.log_label.setText("")

    def UpdateErrorLabel(self, msg):
        self.errorLabel.setText(msg)

    def OnBilgeLevelChanged(self, value: int):
        # update output message
        self.bilge_level = value
        self.levelPercentlabel.setText(f"{value}%")


    def UpdateEngineStatus(self, checked):
        if checked:
            self.engine_status = 1200
        elif self.engOffRadioButton.isChecked():
            self.engine_status = 0

        if self.engine_stat_changed_callback is not None:
            self.engine_stat_changed_callback(self.engine_status)

        print(f"daytime = {self.engine_status}")


def LoadConditions(mode):
    path = "condition_modes/" + mode + ".json"
    with open(path) as f:
        return json.load(f)
