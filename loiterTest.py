__author__ = 'cpaulson'
__author__ = 'cpaulson'
from driver import MAV
import time


class glideSlope():
    def __init__(self):
        print 'Starting MAV'
        self.mav = MAV()
        self.airspeeds = [20,19,18,17,16,15,14,13,12]
        self.count = 0
        self.defaultAirspeed = 15
        self.mav.ahrs2Callback = self.wp_cb

    def wp_cb(self,x):
        print self.count
        if x.seq == 7:
            if self.count >= len(self.airspeeds):
                print 'not tests left'
                pass
            else:

                self.mav.setParam('ARSPD_FBW_MAX', self.airspeeds[self.count]+1.)
                self.mav.setParam('TRIM_ARSPD_CM', self.airspeeds[self.count] * 100) ## Units for this are in cm/2, hence the 100 term
                self.mav.setParam('THR_MAX', 0)
                self.mav.setParam('TECS_SPDWEIGHT', 2)
                print 'Triggering'
                print 'Set Airspeed to {}'.format(self.airspeeds[self.count])
                self.count +=1
        if x.seq == 8:
            self.mav.setParam('THR_MAX', 100)
            self.mav.setParam('TECS_SPDWEIGHT', 1)
            self.mav.setParam('ARSPD_FBW_MAX', 18.0)
            print 'Terminating'
        else:
            pass

    def altitude_cb(self,x):
        if x.altitude< 20:
            self.mav.setParam('THR_MAX', 100)
            self.mav.setParamself.mav.setParam('TRIM_ARSPD_CM', self.defaultAirspeed * 100) ## Units for this are in cm/2, hence the 100 term
            self.mav.setParam('TECS_SPDWEIGHT', 1)
            self.mav.setParam('ARSPD_FBW_MAX', 18.0)
            print 'Altitude Panic!! THR_MAX set to 100'

    def run(self):
        while True:
            time.sleep(5)




test = glideSlope()
test.run()