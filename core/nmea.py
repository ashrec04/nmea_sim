from nmea2000.encoder import NMEA2000Encoder, NMEA2000Message, NMEA2000Field
from nmea2000.decoder import NMEA2000Decoder

WATER_DEPTH_PGN = 128267
WIND_DATA_PGN = 130306

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

        print("ERROR: Sensor type", sensor.name, "is invalid")
        return []

    def GetWaterDepthMsg(self, depth_m):
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
        print("message: ", msg_bytes)
        return msg_bytes

    def GetAnemometerMsg(self, wind_data):
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
        print("message: ", msg_bytes)
        return msg_bytes
    
    def GetSpeedOverGroundMsg(self, speed):
        # Data to encode: Speed over Ground message (PGN 130306)
        message = NMEA2000Message(
            PGN=130306,
            priority=2,
            source=1,
            destination=255,
            fields=[
                NMEA2000Field(
                    id="sid",
                    raw_value=0,
                ),
                NMEA2000Field(
                    id="speed",
                    value=wind_data[0],
                ),
                NMEA2000Field(
                    id="direction",
                    raw_value=wind_data[1],
                ),
                NMEA2000Field(
                    id="refrence",
                    raw_value=0,
                ),
                NMEA2000Field(
                    id="reserved",
                    raw_value=0,
                )
            ]
        )

        msg_bytes = self.encoder.encode_ebyte(message)
        print("message: ", msg_bytes)
        return msg_bytes
     
    def DecodeMessage(self, msg_bytes):
        # Decode the message
        decoded = None
        for b in msg_bytes:
            d = self.decoder.decode_tcp(b)
            if d != None:
                decoded = d
            if decoded:
                print(decoded.PGN, [(fld.id, fld.value) for fld in decoded.fields])
            else:
                print("DECODE ERROR")

