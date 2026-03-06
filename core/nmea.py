from nmea2000.encoder import NMEA2000Encoder, NMEA2000Message, NMEA2000Field
from nmea2000.decoder import NMEA2000Decoder

''' Holds the NEMAMessage Class
    - encodes data from sensors into NMEA2000 messages to be sent by the scheduler
'''

WATER_DEPTH_PGN = 128267
WIND_DATA_PGN = 130306
VESSEL_SPEED_PGN = 129026

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
     
    def DecodeMessage(self, msg_bytes):
        # Decode the message
        decoded = None
        for b in msg_bytes:
            d = self.decoder.decode_tcp(b)
            if d:
                decoded = d
        return decoded

