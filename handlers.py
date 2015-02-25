__author__ = 'cpaulson'

class handlers():
    def __init__(self):
        pass

    def parameter_Handler(self, data):
        self.params[data.param_id.replace('\x00','')] = data.param_value

    def waypoint_Handler(self, data, callback=None):
        if self.currentWP != data.seq:
            self.currentWP = data.seq
            print 'New Waypoint: ', self.currentWP
            if callback:
                callback(data)

    def wind_Handler(self, data):
        self.speed_z = data.speed_z
        self.wind_dir = data.direction

    def vfr_hud_Handler(self, data, callback=None):
        self.climbrate = data.climb
        self.airspeed = data.airspeed
        if callback:
            callback( [data._timestamp, data.climb, data.airspeed, data.alt])

    def ahrs2_Handler(self, data, callback = None):
        self.pitch = data.pitch
        if callback:
            callback([data._timestamp, data.pitch])