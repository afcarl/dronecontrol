#!/usr/bin/env python
# Plot a graph of Data which is comming in on the fly
# uses pylab
# Author: Norbert Feurle
# Date: 12.1.2012
# License: if you get any profit from this then please share it with me
from matplotlib import pyplot
# pyplot.ion()
import numpy as np

class dynamicPlot():
    def __init__(self, q, event, title = None, ylabel = None):
        #Setup queue
        print 'here'
        self.q = q
        self.statusq = event
        # Data Arrays
        self.firstTime = None
        self.x = np.array([])
        self.y = np.array([])

        # Basic Plot Configuration
        self.fig = pyplot.figure(1)

        self.ax = self.fig.add_subplot(111)
        self.ax.autoscale()
        self.ax.grid(True)
        if title:
            self.ax.set_title(title)
        self.ax.set_xlabel("Time")
        if ylabel:
            self.ax.set_ylabel(ylabel)
        self.ax.axis([0,10,-1.5,1.5])
        self.lines = []
        self.line1, = self.ax.plot( self.x, self.y, '-o' )
        self.lines.append( self.line1 )
        self.manager = pyplot.get_current_fig_manager()
        self.manager.canvas.draw()

        self.xmin=None
        self.ymin=None
        self.xmax=None
        self.ymax=None

    def updateData(self):

        while True:
            try:
                item = self.q.get(False)

                if item:
                    if not self.firstTime:
                        self.firstTime = item[0]
                    self.x = np.append(self.x, item[0]-self.firstTime)
                    self.y = np.append(self.y, item[1])
            except Exception,e:
                break


    def updatePlot(self):
        try:
            self.lines[-1].set_data(self.x, self.y)
        except Exception,e:
            pass
            # print Exception,e
        # print self.ax.get_ybound()
        #
        try:
            if not self.xmin or self.x.min() < self.xmin: self.xmin = self.x.min()
            if not self.ymin or self.y.min() < self.ymin: self.ymin = self.y.min()
            if not self.xmax or self.x.max() > self.xmax: self.xmax = self.x.max()
            if not self.ymax or self.y.max() > self.ymax: self.ymax = self.y.max()
        except Exception,e:
            pass
            # print Exception,e

        try:
            self.ax.axis([self.xmin,self.xmax,self.ymin, self.ymax])
        except:
            pass
        self.ax.relim()
        # print self.ax.get_ybound()
        self.ax.autoscale_view()
        self.manager.canvas.draw()
        self.ax.relim()
        # print self.ax.get_ybound()
        self.ax.autoscale_view()
        self.manager.show()
        self.checkStatus()

    def checkStatus(self):
        try:
            item = self.statusq.get(False)
            if item:
                if item == 'terminate':
                    print 'Event is set'
                    self.x = []
                    self.y = []
                    self.firstTime = None
                    self.lines.append( self.ax.plot( self.x, self.y, '-o' )[0] )

        except Exception,e:
            pass


    def waitonEvent(self):
        pass

    def configureTimers(self, interval=500):
        self.timer = self.fig.canvas.new_timer(interval=interval)
        self.timer.add_callback(self.updatePlot)

        self.data_update_timer = self.fig.canvas.new_timer(interval=interval)
        self.data_update_timer.add_callback(self.updateData)

        # self.event_timer = self.fig.canvas.new_timer(interval=interval*5)
        # self.data_update_timer.add_callback(self.updateData)

        self.timer.start()
        self.data_update_timer.start()

    def run(self):
        self.configureTimers()
        pyplot.show()



if __name__=='__main__':
    from multiprocessing import Process, Queue

    q = Queue(100)

    def run():
        d = dynamicPlot(q)
        d.run()

    import time

    p = Process(target=run)
    p.start()

    x = np.linspace(0,6*np.pi, 1000)

    for i in x:
        q.put([i, np.sin(i)])
        time.sleep(.01)


    print 'done'
    p.join()
    exit()