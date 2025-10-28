import random

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
        self.change = config["change_m"]

    def Update(self, now):
        self.last_update = now
        depth = self.mean_depth + random.uniform(-self.change, self.change)
        return {"depth_m": round(depth, 2)}
    

class Anemometer(SensorBase):
    def __init__(self, config):
        super().__init__("anemometer", config["refresh_rate_hz"])
        self.mean_speed = config["mean_speed_kn"]
        self.speed_change = config["speed_change_kn"]
        self.mean_direction = config["mean_direction_deg"]
        self.direction_change = config["direction_change_deg"]

    def Update(self, now):
        self.last_update = now
        speed = self.mean_speed + random.uniform(-self.speed_change, self.speed_change)
        return {"wind_speed_kn": round(speed, 2)}