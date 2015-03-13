__author__ = 'cpaulson'
from apscheduler.schedulers.background import BlockingScheduler
import dill as pickle
import numpy as np
import time

class dataStorage():
    def __init__(self, dataqueue, statusQueue, title=None, dis=None):
        self.x = np.array([])
        self.y = np.array([])
        self.firstTime = None
        self.title= title
        self.dis = dis
        self.scheduler = BlockingScheduler()
        self.dataqueue = dataqueue
        self.statusQueue = statusQueue
        self.dataUpdate_task = self.scheduler.add_job(self.dataUpdate, 'interval', seconds=.1)
        self.eventsUpdate_task = self.scheduler.add_job(self.eventsUpdate, 'interval', seconds=1)
        self.scheduler.start()

    def dataUpdate(self):
        while True:
            try:
                item = self.dataqueue.get(False)
                if item:
                    if not self.firstTime:
                        self.firstTime = item[0]
                    self.x = np.append(self.x, item[0]-self.firstTime)
                    self.y = np.append(self.y, item[1])
                else:
                    break
            except:
                break

    def eventsUpdate(self):
        try:
            item = self.statusQueue.get(False)
            if item:
                if item == 'terminate':
                    print 'Event is set'
                    d2s = {}
                    d2s['title'] = self.title
                    d2s['dis'] = self.dis
                    d2s['x'] = self.x
                    d2s['y'] = self.y
                    try:
                        pickle.dump( d2s, open('{0}time_{1}_value_{2}.pkl'.format(self.path, int(time.time()), self.title),'rb'))
                    except:
                        print 'Failed to dump'

                    self.x = np.array([])
                    self.y = np.array([])
                    self.firstTime = None
        except Exception,e:
            pass


if __name__=='__main__':
    ds = dataStorage(None, None)
