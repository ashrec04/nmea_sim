from nmea2000.encoder import NMEA2000Encoder, NMEA2000Message, NMEA2000Field
from nmea2000.decoder import NMEA2000Decoder

def GenMessage(sensor, reading):
    msg_bytes = "NULL"
    if sensor.name == "depth":
        msg_bytes = GetWaterDepthMsg(reading)
    else:
        print("ERROR: Sensor type", sensor.name, " is invalid")
    
    return msg_bytes

def GetWaterDepthMsg(depth_m):
    # Initialize encoder
    encoder = NMEA2000Encoder()

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

    msg_bytes = encoder.encode_ebyte(message)
    print("message: ", msg_bytes)
    return msg_bytes

def CheckMessage(msg_bytes):
    # Initialize decoder
    decoder = NMEA2000Decoder()

    # Decode the message
    for b in msg_bytes:
        decoded = decoder.decode_tcp(b) or decoded
        print(decoded.PGN, [(fld.id, fld.value) for fld in decoded.fields])

