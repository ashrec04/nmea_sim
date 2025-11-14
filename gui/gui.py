import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from colour_widget import Color


#~~ Global Constants
APPLICATION_NAME = "NMEA 2000 Sim"
WINDOW_HEIGHT = 450
WINDOW_WIDTH = 900

STANDARD_WIDTH = int((WINDOW_WIDTH-100)/2)
LABEL_HEIGHT = int(10*WINDOW_HEIGHT/WINDOW_HEIGHT)
BUTTON_HEIGHT = int((2 * WINDOW_HEIGHT)/9)
BUTTON_WIDTH = int((WINDOW_WIDTH-100)/6)
OPTIONS_HEIGHT = int((5 * WINDOW_HEIGHT)/9)
LOG_HEIGHT = int((7 * WINDOW_HEIGHT)/9)

BUTTON_NAMES = ["Play", "Pause", "Restart"]
SIMULATION_LABEL = "Simulation Modes:"

LOG_LABEL = "Data Log:"

#~~

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APPLICATION_NAME)
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setWindowIcon(QIcon('gui/resources/icon.ico'))
        

        layout_main = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        # sim mode (left)

        # sim mode options
        sim_options = Color("purple")
        sim_options.setFixedSize(STANDARD_WIDTH, OPTIONS_HEIGHT) 
        
        layout_left.addWidget(self.AddLabel(SIMULATION_LABEL, STANDARD_WIDTH, LABEL_HEIGHT))
        layout_left.addWidget(sim_options)
        layout_left.addLayout(self.BuildButtonRow())

        layout_main.addLayout(layout_left)

        # data logger
        log_box = Color("purple")
        log_box.setFixedSize(STANDARD_WIDTH, LOG_HEIGHT)

        layout_right.addWidget(self.AddLabel(LOG_LABEL, STANDARD_WIDTH, LABEL_HEIGHT))
        layout_right.addWidget(log_box)

        layout_main.addLayout(layout_right)

        widget = QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)

    def BuildButtonRow(self):
        layout_buttons = QHBoxLayout()
        for title in BUTTON_NAMES:
            button = QPushButton(title)
            button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
            layout_buttons.addWidget(button)
        return layout_buttons

    def AddLabel(self, text, width, height):
        label = QLabel(text)
        label.setFixedSize(width, height)
        return label

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.