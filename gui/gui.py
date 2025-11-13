import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from colour_widget import Color


#~~ Global Constants
APPLICATION_NAME = "NMEA 2000 Sim"

#~~

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APPLICATION_NAME)
        self.setFixedSize(QSize(900, 450))

        layout_h = QHBoxLayout()
        layout_h2 = QHBoxLayout()
        layout_v1 = QVBoxLayout()
        layout_v2 = QVBoxLayout()

        layout_h2.addWidget(Color("green"))
        layout_h2.addWidget(Color("green"))

        layout_v1.addWidget(Color("blue"))
        layout_v1.addWidget(Color("purple"))
        layout_v1.addLayout(layout_h2)

        layout_h.addLayout(layout_v1)

        layout_v2.addWidget(Color("blue"))
        layout_v2.addWidget(Color("purple"))

        layout_h.addLayout(layout_v2)

        widget = QWidget()
        widget.setLayout(layout_h)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.