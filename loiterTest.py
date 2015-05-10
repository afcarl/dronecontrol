__author__ = 'cpaulson'
from driver import MAV
import time


class glideSlope():
    def __init__(self):
        print 'Starting MAV'
        self.mav = MAV()
        self.mav.vfrCallback = self.altCallback
        self.powered = True

        self.airspeeds = [20,19,18,17,16,15,14,13,12]
        self.count = 0
        self.defaultAirspeed = 15

    def altCallback(self,x):
        print x[3]
        if x[3] > 45:
            if self.powered:
                self.mav.setParam('ARSPD_FBW_MAX', self.airspeeds[self.count]+1.)
                self.mav.setParam('TRIM_ARSPD_CM', self.airspeeds[self.count] * 100) ## Units for this are in cm/2, hence the 100 term
                self.mav.setParam('THR_MAX', 0)
                self.mav.setParam('TECS_SPDWEIGHT', 2)
                self.powered = False
                self.count += 1
                if self.count >= len(self.airspeeds):
                    self.count=0


        if x[3] < 35:
            if not self.powered:
                self.mav.setParam('THR_MAX', 100)
                self.mav.setParam('TECS_SPDWEIGHT', 1)
                self.mav.setParam('ARSPD_FBW_MAX', 18.0)
                # self.mav.setParam('TRIM_ARSPD_CM', self.defaultAirspeed * 100.) ## Units for this are in cm/2, hence the 100 term
                self.powered = True
                print 'Altitude Panic!! THR_MAX set to 100'


    def run(self):
        while True:
            time.sleep(5)




test = glideSlope()
test.run()