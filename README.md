# NMEA2000 Sensor Simulation Program 
NMEA2000 message simulator with GUI using Python 3.14 which generates random data for three simulated sensors (Water Depth, Ananometer and Vessel Speed)

Data is sent via "fast packet" NEMA2000 messages across a [Waveshare USB-CAN-A Bus](https://www.waveshare.com/wiki/USB-CAN-A) plugged into USB Port COM3

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
[usb_can_adapter_v1](https://github.com/RajithaRanasinghe/Python-Class-for-Waveshare-USB-CAN-A/tree/main) is used as a foundation to add a new function which enables the transfer of fast packets

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
