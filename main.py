import asyncio
from qasync import QEventLoop
import sys
import os
from PyQt6.QtWidgets import QApplication
from gui.gui import MainWindow

'''Main entry point for the program
    - initiises GUI and even loop
'''

def main():

    conditions = os.listdir('condition_modes/')
    condition_list = []
    for cond in conditions:
        cond = cond[:-5]
        condition_list.append(cond)


    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    loop = QEventLoop(app) # initises the gui through asyncio
    asyncio.set_event_loop(loop)

    window = MainWindow(condition_list, loop)
    window.show()
    
    with loop:
        loop.run_forever()



if __name__ == "__main__":
    main()