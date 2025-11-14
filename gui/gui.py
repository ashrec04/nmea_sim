import asyncio
import json
import ctypes

from qasync import QEventLoop, asyncSlot

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget

from core.sensors import DepthSensor, Anemometer, SpeedOverGround
from core.scheduler import Scheduler


#~~ Global Constants
APPLICATION_NAME = "NMEA 2000 Sim"
ICON_PATH = 'gui/resources/icon.ico'
WINDOW_HEIGHT = 450
WINDOW_WIDTH = 900
LABEL_HEIGHT = 15

STANDARD_WIDTH = int((WINDOW_WIDTH-100)/2)  # Width of the two main columns
BUTTON_HEIGHT = int((2 * WINDOW_HEIGHT)/9)
BUTTON_WIDTH = int((WINDOW_WIDTH-100)/6)
OPTIONS_HEIGHT = int((5 * WINDOW_HEIGHT)/9)
LOG_HEIGHT = int((7 * WINDOW_HEIGHT)/9)

BUTTON_NAMES = ["Play", "Pause", "Restart"]
SIMULATION_LABEL = "Simulation Modes:"
LOG_LABEL = "Data Log:"

#~~


# Subclass QMainWindow to customise the window
class MainWindow(QMainWindow):

    def __init__(self, loop=None):
        super().__init__()

        self.setWindowTitle(APPLICATION_NAME)
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setWindowIcon(QIcon(ICON_PATH)) # set icon in window
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('nmea-sim.gui') # set icon in taskbar


        self.sim_running = False

        layout_main = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        # sim mode (left)
        layout_left.addWidget(self.AddLabel(SIMULATION_LABEL, STANDARD_WIDTH, LABEL_HEIGHT))
        layout_left.addWidget(self.AddListWidget(["one", "two", "three"] ,STANDARD_WIDTH, OPTIONS_HEIGHT))
        layout_left.addLayout(self.BuildButtonRow())

        layout_main.addLayout(layout_left)

        # data log (right)
        layout_right.addWidget(self.AddLabel(LOG_LABEL, STANDARD_WIDTH, LABEL_HEIGHT))
        layout_right.addWidget(self.AddLabel("THIS IS THE LOG", STANDARD_WIDTH, LOG_HEIGHT))

        layout_main.addLayout(layout_right)

        widget = QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)

        self.loop = loop or asyncio.get_event_loop()

    def BuildButtonRow(self):
        layout_buttons = QHBoxLayout()
        count = 0
        for title in BUTTON_NAMES:
            button = QPushButton(title)
            button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)

            if count == 0: # play
                button.clicked.connect(self.PlayButtonClicked)
            elif count == 1: # pause
                button.clicked.connect(self.PauseButtonClicked)
            else: # restart
                button.clicked.connect(self.RestartButtonClicked)

            layout_buttons.addWidget(button)
            count += 1
        return layout_buttons

    def AddLabel(self, text, width, height):
        label = QLabel(text)
        label.setFixedSize(width, height)
        return label

    def AddListWidget(self, list_options, width, height):
        widget = QListWidget()
        widget.addItems(list_options)
        widget.setFixedSize(width, height)
        return widget

    @asyncSlot()
    async def PlayButtonClicked(self):
        if self.sim_running == True:
            print("simulation already running")
        else:
            self.sim_running = True
            print("simulation start")

            config = self.LoadConditions("condition_modes/calm.json")
            sensors = [
                DepthSensor(config["sensors"]["depth"]),
                Anemometer(config["sensors"]["anemometer"]),
                SpeedOverGround(config["sensors"]["speed over ground"])
            ]


            scheduler = Scheduler(config["tick_rate_hz"], sensors, self.loop)
            await scheduler.run(duration_s=10)
            

    def PauseButtonClicked(self):
        if self.sim_running == True:
            self.sim_running = False
            print("simulation paused")
        else:
            self.sim_running = False
            print("simulation already stopped")

    def RestartButtonClicked(self):
        if self.sim_running == True:
            self.sim_running = True
            print("simulation restarted")
        else:
            self.sim_running = False
            print("simulation not running")

    def LoadConditions(self, path):
        with open(path) as f:
            return json.load(f)