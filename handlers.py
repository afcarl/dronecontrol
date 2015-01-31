__author__ = 'cpaulson'

class handlers():
    def __init__(self):
        pass

    def parameter_Handler (self, data):
        self.params[data.param_id.replace('\x00','')] = data.param_value

    def waypoint_Handler(self, data, callback=None):
        if self.currentWP != data.seq:
            self.currentWP = data.seq
            print 'New Waypoint: ', self.currentWP
        if callback:
            callback(data)