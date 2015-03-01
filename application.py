__author__ = 'cpaulson'
from multiprocessing import Queue, Pool, Process, Event
from multiprocessing.pool import ThreadPool
from plotTest import dynamicPlot
from driver import MAV
import numpy as np
import time
import dill as pickle

def f(value, event):
    d = dynamicPlot(value, event)
    d.run()


class glideApplication():
    def __init__(self):
        self.airspeedq = Queue(100)
        self.pitchq = Queue(100)
        self.climbq = Queue(100)
        self.spdweight = [0,1,2]
        self.sinkrate = [10,9,8,7,6,5,4,3,2,1]
        self.airspeeds = [15,14,13,12,11,10,9]
        self.event = Event()
        self.count = 0
        self.broadcastQueues = []
        self.plots = {'airspeed':self.airspeedq, 'pitch':self.pitchq, 'climb':self.climbq}
        for i in self.plots:
            self.broadcastQueues.append(Queue())
            p = Process(target=f, args=(self.plots[i], self.broadcastQueues[-1]))
            p.start()
        time.sleep(5)


    def run(self):
        self.mav = MAV()
        time.sleep(15)
        print self.mav.params['TRIM_ARSPD_CM']
        print self.mav.params['GLIDE_SLOPE_MIN']
        self.mav.waypointCallback = self.wp_cb
        while True:
            time.sleep(5)

        self.mav.close()

        print 'done'
        # p.join()
        self.pool.join()

    def broadcast(self, value):
        for q in self.broadcastQueues:
            q.put(value)

    def vfrcb(self, x):
        self.airspeedq.put([x[0],x[2]])
        self.climbq.put([x[0],x[3]])
        if x[3]< 25:
            print x[3]
            print 'Too low!!!'
            self.mav.setParam('THR_MAX', 100)

    def ahrs2cb(self, x):
        self.pitchq.put([x[0],np.degrees(x[1])])

    def wp_cb(self, x):
        if x.seq == 3:
            print 'Triggering'
            self.mav.vfrCallback = self.vfrcb
            self.mav.ahrs2Callback = self.ahrs2cb
            self.mav.setParam('TECS_SPDWEIGHT', 0)
            self.mav.setParam('TECS_PTCH_DAMP', 1)
            self.mav.setParam('PTCH2SRV_RMAX_UP', 1.5 )
            print 'Setting min airspeed to: {}'.format(self.airspeeds[self.count])
            # self.mav.setParam('TECS_SINK_MAX', self.sinkrate[self.count])
            self.mav.setParam('ARSPD_FBW_MIN', self.airspeeds[self.count])
            self.mav.setParam('THR_MAX', 0)
        if x.seq == 4:
            self.count +=1
            self.mav.setParam('PTCH2SRV_RMAX_UP', 0 )
            self.mav.setParam('THR_MAX', 100)
            self.mav.setParam('TECS_SPDWEIGHT', 1)
            self.mav.setParam('TECS_PTCH_DAMP', 0)
            print 'Terminating'
            self.mav.vfrCallback = None
            self.mav.ahrs2Callback = None
            self.broadcast('terminate')
        else:
            pass


ga = glideApplication()
ga.run()

