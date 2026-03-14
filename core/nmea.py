from nmea2000.encoder import NMEA2000Encoder, NMEA2000Message, NMEA2000Field
from nmea2000.decoder import NMEA2000Decoder

''' Holds the NEMAMessage Class
    - encodes data from sensors into NMEA2000 messages to be sent by the scheduler
'''

WATER_DEPTH_PGN = 128267
WIND_DATA_PGN = 130306
VESSEL_SPEED_PGN = 129026
FLUID_LEVEL_PGN = 127505
ENGINE_PARAMS_PGN = 127488

BILGE_TANK_CAPACITY_L = 15  # arbitrary capacity for bilge tank
FLUID_TYPE_WATER = 1         # TANK_TYPE value for water


class NEMAMessage:
    def __init__ (self):
        #initise encoder and decoder
        self.encoder = NMEA2000Encoder()
        self.decoder = NMEA2000Decoder()

    def GenMessage(self, sensor, reading):
        if sensor.name == "depth":
            msg = self.GetWaterDepthMsg(reading[0])
        elif sensor.name == "anemometer":
            msg = self.GetAnemometerMsg(reading)
        elif sensor.name == "vessel speed":
            msg = self.GetVesselSpeedMsg(reading[0])
        elif sensor.name == "bilge level":
            msg = self.GetFluidLevelMsg(reading[0])
        elif sensor.name == "engine diagnostics":
            msg = self.GetEngineDiagnosticMsg(reading[0])
        else:
            print("ERROR: Sensor type", sensor.name, "is invalid")
            return []
        
        encoded = self.encoder.encode_usb(msg)
        return encoded, msg

    def GetWaterDepthMsg(self, depth_m):
        try:
            message = NMEA2000Message(
                PGN= WATER_DEPTH_PGN,
                priority=2,
                source=1,
                destination=255,
                fields=[
                    NMEA2000Field(
                        id="sid",
                        raw_value=0,
                    ),
                    NMEA2000Field(
                        id="depth",
                        value=depth_m,
                    ),
                    NMEA2000Field(
                        id="offset",
                        raw_value=0,
                    ),
                    NMEA2000Field(
                        id="range",
                        raw_value=100,
                    )
                ]
            )

        except Exception as e: 
            print("ERROR IN MESSAGE: ", e)
        return message

    def GetAnemometerMsg(self, wind_data):
        try:
            message = NMEA2000Message(
                PGN=WIND_DATA_PGN,
                priority=2,
                source=1,
                destination=255,
                fields=[
                    NMEA2000Field(
                        id="sid",
                        raw_value=0,
                    ),
                    NMEA2000Field(
                        id="windSpeed",
                        value=wind_data[0],
                    ),
                    NMEA2000Field(
                        id="windAngle",
                        raw_value=wind_data[1],
                    ),
                    NMEA2000Field(
                        id="reference",
                        raw_value=0,
                    ),
                    NMEA2000Field(
                        id="reserved_43",
                        raw_value=0,
                    )
                ]
            )

        except Exception as e: 
            print("ERROR IN MESSAGE: ", e)
        
        return message
    
    def GetVesselSpeedMsg(self, sog):
        # Data to encode: Vessel Speed message (PGN 129026)
        try:
            message = NMEA2000Message(
                PGN=VESSEL_SPEED_PGN,
                priority=2,
                source=1,
                destination=255,
                fields=[
                    NMEA2000Field(
                        id="sid",
                        raw_value=0,
                    ),
                    NMEA2000Field(
                        id="cogReference",
                        value=0,
                    ),
                    NMEA2000Field(
                        id="reserved_10",
                        raw_value=0,
                    ),
                    NMEA2000Field(
                        id="cog",
                        raw_value=0,
                    ),
                    NMEA2000Field(
                        id="sog",
                        value=sog,
                    ),
                    NMEA2000Field(
                        id="reserved_48",
                        raw_value=0,
                    )
                    ]
                )

        except Exception as e: 
            print("ERROR IN MESSAGE: ", e)

        return message
     
    def GetFluidLevelMsg(self, level, instance=0):
        # Data to encode: Fluid Level (PGN 127505) for bilge water level
        try:
            message = NMEA2000Message(
                PGN=FLUID_LEVEL_PGN,
                priority=2,
                source=1,
                destination=255,
                fields=[
                    NMEA2000Field(
                        id="instance",
                        value=instance,
                    ),
                    NMEA2000Field(
                        id="type",
                        raw_value=FLUID_TYPE_WATER,
                    ),
                    NMEA2000Field(
                        id="level",
                        value=level,
                    ),
                    NMEA2000Field(
                        id="capacity",
                        value=BILGE_TANK_CAPACITY_L,
                    ),
                    NMEA2000Field(
                        id="reserved_56",
                        raw_value=0,
                    )
                    ]
                )

        except Exception as e: 
            print("ERROR IN MESSAGE: ", e)
            message = None

        return message

    def GetEngineDiagnosticMsg(self, rpm, instance=0, pressure = 1000, trim = 0):
        # Data to encode: Engine Diagnostics (PGN 127488) only thing being change is the rpm
        # in gui:
        # when engine off: rpm = 0
        # when engine On: rpm = 12000
        try:
            message = NMEA2000Message(
                PGN=ENGINE_PARAMS_PGN,
                priority=2,
                source=1,
                destination=255,
                fields=[
                    NMEA2000Field(
                        id="instance",
                        value=0,
                    ),
                    NMEA2000Field(
                        id="speed",
                        value=rpm,
                    ),
                    NMEA2000Field(
                        id="boostPressure",
                        value=pressure,
                    ),
                    NMEA2000Field(
                        id="tiltTrim",
                        value=trim,
                    ),
                    NMEA2000Field(
                        id="reserved_48",
                        raw_value=0,
                    )
                    ]
                )

        except Exception as e: 
            print("ERROR IN MESSAGE: ", e)
            message = None

        return message


    def DecodeMessage(self, msg_bytes):
        # Decode the message
        decoded = None
        for b in msg_bytes:
            d = self.decoder.decode_tcp(b)
            if d:
                decoded = d
        return decoded

