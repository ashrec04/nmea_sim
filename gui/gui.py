import asyncio
import json
import ctypes

from qasync import QEventLoop, asyncSlot

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QScrollArea

from core.sensors import DepthSensor, Anemometer, VesselSpeed
from core.scheduler import Scheduler


#~~ Global Constants
APPLICATION_NAME = "NMEA 2000 Sim"
ICON_PATH = 'gui/resources/icon.ico'
WINDOW_HEIGHT = 450
WINDOW_WIDTH = 1200
LABEL_HEIGHT = 15
SCROLL_BAR_WIDTH = 10

SIM_WIDTH = int((WINDOW_WIDTH-100)/3)  # Width of the sim column
LOG_WIDTH = int(2*(WINDOW_WIDTH-100)/3)  # Width of the log column
BUTTON_HEIGHT = int((2 * WINDOW_HEIGHT)/9)
BUTTON_WIDTH = int((WINDOW_WIDTH-100)/6)
OPTIONS_HEIGHT = int((5 * WINDOW_HEIGHT)/9)
LOG_HEIGHT = int((7 * WINDOW_HEIGHT)/9)

BUTTON_NAMES = ["Start", "Stop"]
SIMULATION_LABEL_TITLE = "Simulation Modes:"
LOG_LABEL_TITLE = "Data Log:"

#~~

# Subclass QMainWindow to customise the window
class MainWindow(QMainWindow):

    def __init__(self, condition_list, loop=None):
        super().__init__()

        self.mode_chosen = None

        # setup app window
        self.setWindowTitle(APPLICATION_NAME)
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setWindowIcon(QIcon(ICON_PATH)) # set icon in window
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('nmea-sim.gui') # set icon in taskbar
        # 

        self.sim_running = False # TODO: make redundant

        # three widgets for app window
        layout_main = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()
        #

        # sim mode widgets (left)
        layout_left.addWidget(self.AddLabel(SIMULATION_LABEL_TITLE, SIM_WIDTH, LABEL_HEIGHT))
        layout_left.addWidget(self.AddListWidget(condition_list ,SIM_WIDTH, OPTIONS_HEIGHT))
        layout_left.addLayout(self.BuildButtonRow())

        layout_main.addLayout(layout_left)
        #

        # data log widgets (right)
        layout_right.addWidget(self.AddLabel(LOG_LABEL_TITLE, LOG_WIDTH, LABEL_HEIGHT))

        self.log_label = self.AddLabel("", LOG_WIDTH)

        scroll = QScrollArea() # scroll bar for data log
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.log_label)
        layout_right.addWidget(scroll)
        #
        layout_main.addLayout(layout_right)

        widget = QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)

        
        self.loop = loop or asyncio.get_event_loop()
        self.log_queue = asyncio.Queue()
        self.loop.create_task(self.UpdateLogLabel())
        self.scheduler = None

    def BuildButtonRow(self):
        layout_buttons = QHBoxLayout()
        count = 0
        for title in BUTTON_NAMES:
            button = QPushButton(title)
            button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)

            if count == 0: # play
                button.clicked.connect(self.PlayButtonClicked)
            elif count == 1: # pause
                button.clicked.connect(self.StopButtonClicked)
            else: # restart
                button.clicked.connect(self.RestartButtonClicked)

            layout_buttons.addWidget(button)
            count += 1
        return layout_buttons

    def AddLabel(self, text, width, height=None):
        label = QLabel(text)
        if height:
            label.setFixedSize(width, height)
        else:
            label.setFixedWidth(LOG_WIDTH)
        return label

    def AddListWidget(self, list_options, width, height):
        widget = QListWidget()
        widget.addItems(list_options)
        widget.setFixedSize(width, height)
        widget.currentItemChanged.connect(self.ModeChosen)
        return widget

    def ModeChosen(self, m):
        self.mode_chosen = m.text()

    @asyncSlot()
    async def PlayButtonClicked(self):
        if self.sim_running == True:
            print("simulation already running")
        else:
            config = LoadConditions(self.mode_chosen)
            sensors = [
                DepthSensor(config["sensors"]["depth"]),
                Anemometer(config["sensors"]["anemometer"]),
                VesselSpeed(config["sensors"]["vessel speed"])
            ]

            self.scheduler = Scheduler(config["tick_rate_hz"], sensors, self.loop, self.log_queue)
            try:
                self.ResetLogLabel()
                self.sim_running = True
                await self.scheduler.Run(duration_s=10)
                
            except Exception as e:
                self.sim_running = False
                print("ERROR: scheduler has encountered an issue ", e)
            
    @asyncSlot()
    async def StopButtonClicked(self):
        if self.sim_running == True:
            await self.scheduler.Stop()
            self.sim_running = False
            print("simulation stopped")
        else:
            self.sim_running = False
            print("simulation already stopped")

    async def UpdateLogLabel(self):
        while True:
            message = await self.log_queue.get()
            self.log_label.setText((self.log_label.text() + "\n" + message).strip())
            self.log_queue.task_done()
    
    def ResetLogLabel(self):
        self.log_label.setText("")



def LoadConditions(mode):
    path = "condition_modes/" + mode + ".json"
    print(path)
    with open(path) as f:
        return json.load(f)