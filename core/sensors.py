import numpy as np

'''
Holds Sensors classes that generate data for the scheduler to send as NMEA messages
'''

#Basic Sensor class for subs to inherit
class SensorBase:
    #constructor
    def __init__(self, name, refresh_rate_hz):
        self.name = name
        self.refresh_rate_hz = refresh_rate_hz
        self.last_refresh_hz = 0
        self.last_sensor_reading = 0
    
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
        self.variation = config["variation_m"]
        self.last_sensor_reading = config["mean_depth_m"]

    def Update(self, now):
        self.last_update = now
        
        #-------------------------------------------------------------------------#
        #uses the following formula to create a random variation in sensor reading
        # μ + d*sin(t) + sin(r*t)
        # Where:
        # μ = mean depth
        # d = depth variation
        # t = current time
        # r = random integer between -5 and 5
        #-------------------------------------------------------------------------#

        return [round((self.mean_depth + self.variation * np.sin(now) + np.sin(now*np.random.randint(low=-2, high=2))), 1)]


class Anemometer(SensorBase):
    def __init__(self, config):
        super().__init__("anemometer", config["refresh_rate_hz"])
        self.mean_speed = config["mean_speed_kn"]
        self.speed_variation = config["speed_variation_kn"]
        self.mean_direction = config["mean_direction_deg"]
        self.direction_variation = config["direction_variation_deg"]

    def Update(self, now):
        self.last_update = now
        return [
            round(self.mean_speed + self.speed_variation * np.sin(now) + np.sin(now*np.random.randint(low=-5, high=5)), 1),
            round(self.mean_direction + self.direction_variation * np.sin(now) + np.sin(now*np.random.randint(low=-5, high=5)))
            ]


class VesselSpeed(SensorBase):
    def __init__(self, config):
        super().__init__("vessel speed", config["refresh_rate_hz"])
        self.mean_speed = config["mean_speed_kn"]
        self.speed_variation = config["speed_variation_kn"]

    def Update(self, now):
        self.last_update = now
        if self.mean_speed != 0: # allows anchored condition to work (no negative numbers passed)
            return [round(self.mean_speed + self.speed_variation * np.sin(now) + np.sin(now*np.random.randint(low=-5, high=5)), 1)]
        else:
            return [np.float64(self.mean_speed)]


class BilgeStatus(SensorBase):
    def __init__(self, level_provider, refresh_rate_hz = 0.1):
        super().__init__("bilge level", refresh_rate_hz=refresh_rate_hz)
        self.level_provider = level_provider # get level from gui

    def Update(self, now):
        self.last_update = now
        try:
            raw_level = self.level_provider() if callable(self.level_provider) else self.level_provider
        except Exception:
            raw_level = 0
        
        level_percent = max(0, min(100, int(raw_level))) # clamp to 0-100%
        return [level_percent]


class EngineStatus(SensorBase):
    def __init__(self, rpm, refresh_rate_hz = 0.1):
        super().__init__("engine diagnostics", refresh_rate_hz=refresh_rate_hz)
        self.rpm = rpm # get rpm from gui

    def Update(self, now):
        self.last_update = now
        try:
            raw_level = self.rpm() if callable(self.rpm) else self.rpm
        except Exception:
            raw_level = 0

        return [raw_level]