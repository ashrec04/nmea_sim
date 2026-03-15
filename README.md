# NMEA2000 Sensor Simulation Program 
NMEA2000 message simulator interacted with using a GUI which generates random data for the following simulated sensors and diganostics:
- Water Depth
- Anemometer
- Vessel Speed
- Bilge Information
- Engine Information

Data is sent via 20 Byte NEMA2000 messages across a [Waveshare USB-CAN-A Bus](https://www.waveshare.com/wiki/USB-CAN-A)

## Libraries Used
```
nmea2000
PyQt6
qasync
asyncio
json
numpy
time
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
│   ├───anchored.json
│   ├───breezy.json
│   ├───calm.json
│   ├───gale.json
│   ├───gentle.json
│   └───storm.json
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
