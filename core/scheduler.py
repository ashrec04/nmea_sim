import asyncio
import time
from core.nmea import NEMAMessage
from core.usb_can_adapter_v1 import UsbCanAdapter

''' Scheduler class runs the main loop of the program
    - Checks each sensor for updates
    - Sends messages over the CAN bus
'''
COM_PORTS = ["COM3","COM5"] # COM port options on pc for CAN adapter
COM_THREE = 0
COM_FIVE = 1

class Scheduler:
    def __init__(self, tick_rate_hz, sensors, loop = None, log_queue = None):
        self.tick_time_s = 1 / tick_rate_hz
        self.sensors = sensors
        self.running = False
        self.sim_started = False
        self.loop = loop or asyncio.get_event_loop()
        self.log_queue = log_queue

        self.uca = None

    
    def SetRun(self):
        if not self.sim_started:
            self.sim_started = True
            self.running = True
            self.OpenCan()

    #initise run
    async def Run(self, duration_s = None):
        self.SetRun()
        start_time = time.time()
        sim_tick = 0
        n2k = NEMAMessage()

        while self.running:
            now = time.time()
            for sensor in self.sensors:
                if sensor.ShouldUpdate(now):
                    reading = sensor.Update(now)

                    message_frames, n2k_msg = n2k.GenMessage(sensor, reading)
                    decoded_message = n2k_msg
                    self.SendData(message_frames, decoded_message)  

                    if message_frames and self.log_queue:
                        entry = f"PGN {decoded_message.PGN}: {[(fld.id, fld.value) for fld in decoded_message.fields]}" # add to log
                        await self.log_queue.put(entry)
            
            sim_tick += 1

            await asyncio.sleep(self.tick_time_s)
            if duration_s and ((time.time() - start_time) > duration_s):
                break
    
    def OpenCan(self):

        # ============== #
        # Opens CAN Port #
        # ============== #

        if self.uca:    # if coms already open
            return
        
        self.uca = UsbCanAdapter()  # declare CAN comm obj


        port = self.uca.adapter_init(COM_PORTS[COM_THREE])   #try open com port COM3 first

        if port is None or not port.is_open:    #try open com port COM5
            port = self.uca.adapter_init(COM_PORTS[COM_FIVE])
        
        if port is None or not port.is_open:    # COM port not found, produce error
            raise RuntimeError("Failed to open CAN Com Port")
        
        self.uca.command_settings(speed=125000) # set baud rate (125K for NMEA2k)


    async def Stop(self):

        # ======================================= #
        # Closes can port and stops the main loop #
        # ======================================= #

        self.running = False
        self.sim_started = False
        if self.uca:
            self.uca.adapter_close()
            self.uca = None


    def SendData(self, frames, decoded):

        # ====================================================================== #
        # frames: list of 8-byte fast-packet chunks from NEMAMessage.GenMessage()
        # decoded: decoded message (PGN, priority, source)
        # ====================================================================== #
            
        try:
            if not frames or decoded is None or self.uca is None:
                return
            
            # Build 29 bit CAN ID: priority (3 bits), PGN (18 bits), source (8 bits)
            can_id = ((decoded.priority & 0x7) << 26) | ((decoded.PGN & 0x3FFFF) << 8) | (decoded.source & 0xFF)
            print(can_id, " : ", frames)

            for frame in frames:
                self.uca.send_data_frame(can_id, frame)  # 29-bit ID → extended frame automatically

        except Exception as e:
            print(f"Error sending message over CAN bus: {e}")