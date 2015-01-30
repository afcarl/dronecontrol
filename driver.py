import time
from pymavlink import mavutil
from threading import Thread, Lock

class MAV():
    def __init__(self):
        ## Connect to the mavlink proxy with udp, will work for STIL and on the real system
        self.msrc = mavutil.mavlink_connection('udp:localhost:14550', planner_format=True, notimestamps=True,robust_parsing=True)
        self.msrc.wait_heartbeat()
        self.mode = self.msrc.flightmode

        ## We might go mutlithread, lets setup a lock on comms
        self.comm_lock = Lock()

        # Grab all parameters
        self.params = {}
        self.msrc.param_fetch_all() #params will be filled by the callback function

        # Configure the monitor thread
        self.threadEnd = False #Helps with a clean exit
        self.thread = Thread(target=self.monitorThread)
        self.thread.daemon = True
        self.thread.start()

    def setParam(self, parameter, value):
        tryCount = 5
        while tryCount > 0:
            self.msrc.param_set_send(parameter, value)
            time.sleep(0.05)
            if value != self.params[parameter]:
                print 'param write failed, trying again'
                tryCount -=1
                time.sleep(.1)
            else:
                print '{0} set to {1}, requested value {2}'.format(parameter, self.params[parameter], value)
                break

    def setAuto(self):
        self.msrc.set_mode_auto()
    def setManual(self):
        self.msrc.setManual()
    def setRTL(self):
        self.msrc.setRTL()

    def monitorThread(self):
        while not self.threadEnd:
            l = self.msrc.recv_match()
            if l:
                self.messageCallback(l)
            else:
                time.sleep(0.01)

    def messageCallback(self, data):
        '''
        Manages the callback for incoming messages
        :param data: the message data
        :return: Nothing, all changes are stored in self
        '''
        if data._type is 'PARAM_VALUE':
            self.params[data.param_id.replace('\x00','')] = data.param_value
        # if data._type == 'SYS_STATUS':
        #     print data
        #     # self.flightmode = mavutil.mode_string_v09(data)
        #     # print 'Flight Mode: ', self.flightmode
        # else:
        #     print data
    def close(self):
        self.threadEnd = True
        self.thread.join()
        print 'Everything closed, exiting now...'


if __name__=='__main__':
    print 'Starting MAV'
    mav = MAV()
    #allow some time for startup
    #TODO: turn startup wait into a function with checking
    time.sleep(20)

    for i in range(5):
        mav.setParam('THR_MAX', i*20.0)
        time.sleep(5)
    print mav.params
    mav.close()
    print 'Here!'