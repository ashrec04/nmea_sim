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



#~~

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APPLICATION_NAME)
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setWindowIcon(QIcon('gui/resources/icon.ico'))
        

        layout_main = QHBoxLayout()
        layout_buttons = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        # pause, play buttons
        play_button = QPushButton("Play")
        play_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)

        pause_button = QPushButton("Pause")
        pause_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)

        restart_button = QPushButton("Restart")
        restart_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)

        layout_buttons.addWidget(play_button)
        layout_buttons.addWidget(pause_button)
        layout_buttons.addWidget(restart_button)


        # sim mode side
        # title
        sim_title = QLabel("Simulation Mode:")
        sim_title.setFixedSize(STANDARD_WIDTH, LABEL_HEIGHT) 

        # sim mode options
        sim_options = Color("purple")
        sim_options.setFixedSize(STANDARD_WIDTH, OPTIONS_HEIGHT) 
        
        layout_left.addWidget(sim_title)
        layout_left.addWidget(sim_options)
        layout_left.addLayout(layout_buttons)

        layout_main.addLayout(layout_left)

        # data logger
        log_title = QLabel("Data Log:")
        log_title.setFixedSize(STANDARD_WIDTH, LABEL_HEIGHT)

        log_box = Color("purple")
        log_box.setFixedSize(STANDARD_WIDTH, LOG_HEIGHT)

        layout_right.addWidget(log_title)
        layout_right.addWidget(log_box)

        layout_main.addLayout(layout_right)

        widget = QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.