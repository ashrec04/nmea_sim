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
```

## File Structure
```  
nmea_sim
├── .gitattributes
├── .gitignore
├── main.py
├── README.md
├── condition_modes
│   └── calm.json     
├── core
│   ├── nmea.py
│   ├── scheduler.py
│   └── sensors.py          
└── gui
    ├── colour_widget.py
    └── gui.py
nmea_sim
├──.gitattributes
├──.gitignore
├──main.py
├──README.md
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
        └───icon.ico
```
