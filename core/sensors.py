import random
import time
import math

#Basic Sensor class for subs to inherit
class SensorBase:
    #constructor
    def __init__(self, name, refresh_rate_hz):
        self.name = name
        self.refresh_rate_hz = refresh_rate_hz
        self.last_refresh_hz = 0
    
    #true or false return
    def ShouldUpdate(self, time_now):
        return time_now - self.last_refresh_hz >= self.refresh_rate_hz
    
    #empty in parent class but made a required declarable in all sub classes
    def Update(self, now):
        raise NotImplementedError("ERROR: Subclasses must implement this method")


class DepthSensor(SensorBase):

    def __init__(self, config):
        super().__init__("depth", config["refresh_rate_hz"])
        self.mean_depth = config["mean_depth_m"]
        self.noise = config["noise_m"]

    #Get new random depth and update latest refresh
    def Update(self, now):
        self.last_update = now
        depth = self.mean_depth + random.uniform(-self.noise, self.noise)
        return {"depth_m": round(depth, 2)}