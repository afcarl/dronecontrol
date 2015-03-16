__author__ = 'cpaulson'

from driver import MAV
from multiprocessing import Process, Queue, Event
import time
import numpy as np
from dataStorage import dataStorage as DS

def f(dataQueue, eventQueue, title, dis):
    d = DS(dataQueue, eventQueue, title=title, dis=dis)
    d.run()



class glideApplication():
    def __init__(self):
        self.airspeed_queue = Queue(100)
        self.pitch_queue = Queue(100)
        self.alt_queue = Queue(100)
        self.airspeeds = [15,14,13,12,11,10,9]
        self.event = Event()
        self.count = 0
        self.broadcastQueues = []
        time.sleep(5)
        self.datastores = {'airspeed':{'queue':self.airspeed_queue, 'title': 'Airspeed', 'dis':'Airspeed (m/s)'},\
              'pitch':{'queue':self.pitch_queue, 'title': 'Pitch', 'dis':'Pitch Angle (deg)'},\
              'climb':{'queue':self.alt_queue, 'title': 'Altitude', 'dis':'Altitude (m)'} }
        for i in self.datastores:
            self.broadcastQueues.append(Queue())
            p = Process(target=f, args=(self.datastores[i]['queue'], self.broadcastQueues[-1],self.datastores[i]['title'],self.datastores[i]['dis'] ))
            p.start()
        time.sleep(5)


    def run(self):
        self.mav = MAV()
        time.sleep(15)
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
        self.airspeed_queue.put([x[0],x[2]])
        self.alt_queue.put([x[0],x[3]])
        if x[3]< 20:
            print x[3]
            print 'Too low!!!'
            self.mav.setParam('THR_MAX', 100)

    def ahrs2cb(self, x):
        self.pitch_queue.put( [x[0], np.degrees(x[1]) ] )

    def wp_cb(self, x):
        if x.seq == 6:
            print 'Triggering'
            self.mav.vfrCallback = self.vfrcb
            self.mav.ahrs2Callback = self.ahrs2cb
            self.mav.setParam('TECS_SPDWEIGHT', 2)
            # self.mav.setParam('TECS_PTCH_DAMP', 0)
            # self.mav.setParam('PTCH2SRV_RMAX_UP', 2 )
            # self.mav.setParam('PTCH2SRV_TCONST', .7)
            # self.mav.setParam('PTCH2SRV_P', 5)
            # self.mav.setParam('PTCH2SRV_I', 0.05)
            # self.mav.setParam('PTCH2SRV_D', 0.05)
            # self.mav.setParam('PTCH2SRV_RMAX_DOWN', 3 )
            print 'Setting min airspeed to: {}'.format(self.airspeeds[self.count])
            # self.mav.setParam('TECS_SINK_MAX', self.sinkrate[self.count])
            self.mav.setParam('ARSPD_FBW_MIN', self.airspeeds[self.count])
            self.mav.setParam('THR_MAX', 0)
        if x.seq == 7:
            self.count +=1
            # self.mav.setParam('PTCH2SRV_RMAX_UP', 0 )
            self.mav.setParam('THR_MAX', 100)
            self.mav.setParam('TECS_SPDWEIGHT', 1)
            # self.mav.setParam('TECS_PTCH_DAMP', 0)
            print 'Terminating'
            self.mav.vfrCallback = None
            self.mav.ahrs2Callback = None
            time.sleep(1)
            self.broadcast('terminate')
        else:
            pass

if __name__=='__main__':
    ga = glideApplication()
    ga.run()
