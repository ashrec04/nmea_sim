from nmea2000.encoder import NMEA2000Encoder, NMEA2000Message, NMEA2000Field
from nmea2000.decoder import NMEA2000Decoder

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
            return self.GetWaterDepthMsg(reading[0])
        elif sensor.name == "anemometer":
            return self.GetAnemometerMsg(reading)
        elif sensor.name == "vessel speed":
            return self.GetVesselSpeedMsg(reading)

        print("ERROR: Sensor type", sensor.name, "is invalid")
        return []

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

            msg_bytes = self.encoder.encode_ebyte(message)

        except Exception as e: 
            print("ERROR IN MESSAGE: ", e)
        return msg_bytes

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

            msg_bytes = self.encoder.encode_ebyte(message)

        except Exception as e: 
            print("ERROR IN MESSAGE: ", e)
        
        return msg_bytes
    
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
                    raw_value=sog,
                ),
                NMEA2000Field(
                    id="reserved_48",
                    raw_value=0,
                )
                ]
            )

            msg_bytes = self.encoder.encode_ebyte(message)

        except Exception as e: 
            print("ERROR IN MESSAGE: ", e)

        return msg_bytes
     
    def DecodeMessage(self, msg_bytes):
        # Decode the message
        decoded = None
        for b in msg_bytes:
            d = self.decoder.decode_tcp(b)
            if d:
                decoded = d
        return decoded

