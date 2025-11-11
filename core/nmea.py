from nmea2000.encoder import NMEA2000Encoder, NMEA2000Message, NMEA2000Field
from nmea2000.decoder import NMEA2000Decoder

class NEMAMessage:
    def __init__ (self):
        #initise encoder and decoder
        self.encoder = NMEA2000Encoder()
        self.decoder = NMEA2000Decoder()

    def GenMessage(self, sensor, reading):
        if sensor.name == "depth":
            return self.GetWaterDepthMsg(float(reading))

        print("ERROR: Sensor type", sensor.name, "is invalid")
        return []

    def GetWaterDepthMsg(self, depth_m):
        # Data to encode: Water Depth message (PGN 128267)
        message = NMEA2000Message(
            PGN=128267,
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

