from nmea2000.encoder import NMEA2000Encoder, NMEA2000Message, NMEA2000Field
from nmea2000.decoder import NMEA2000Decoder
import itertools

''' Holds the NEMAMessage class which encodes
    data from sensors into NMEA2000 messages
    for the scheduler to send
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
            msg = self.GetVesselSpeedMsg(reading)
        else:
            print("ERROR: Sensor type", sensor.name, "is invalid")
            return []
        
        '''
        payload = self.encoder.encode_raw(msg)  #gets the concatenated data bytes for the PGN

        #Slices msg into fast-packet frames
        seq = next(itertools.cycle(range(8)))
        frames = []
        total = len(payload)

        #first frame
        chunk0 = payload[:6]
        frames.append(bytes([(seq << 5) | 0, total, *chunk0.ljust(6, b"\xff")]))

        # subsequent frames
        rest = payload[6:]
        for i in range(1, (len(rest) + 6) // 7 + 1):
            chunk = rest[(i-1)*7 : i*7]
            frames.append(bytes([(seq << 5) | i, *chunk.ljust(7, b"\xff")]))
        '''
        
        frames = self.encoder._encode(msg)
        return frames, msg

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

            # msg_bytes = self.encoder.encode_ebyte(message)

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

            # msg_bytes = self.encoder.encode_ebyte(message)

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
                        raw_value=sog,
                    ),
                    NMEA2000Field(
                        id="reserved_48",
                        raw_value=0,
                    )
                    ]
                )

            # msg_bytes = self.encoder.encode_ebyte(message)

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

