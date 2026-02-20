### nmea_sim
nmea2000 message simulator with GUI using Python 3.14

## Libraries Used
```
numpy
asyncio
json
time
PyQt6
nmea2000
qasync
```

## Code Used
[usb_can_adapter_v1](https://github.com/RajithaRanasinghe/Python-Class-for-Waveshare-USB-CAN-A/tree/main) the script usesed this code with a new function to enable the transfer of fast packets

## File Structure
```  
nmea_sim
├───.gitattributes
├───.gitignore
├───main.py
├───README.md
├───condition_modes
│   ├──calm.json
│   └──mild.json
├───core
│   ├───nmea.py
│   ├───scheduler.py
│   ├───sensors.py
│   └───usb_can_adapter_v1.py
└───gui
    ├───gui.py
    └───resources
        ├───icon.ico
        └───mainwindow.ui
```
