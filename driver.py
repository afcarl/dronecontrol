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
        '''

        :param parameter:
        :param value:
        :return: Nothing
        '''
        #TODO: Return True or False based on verification and validation
        #TODO: Add better error management here

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
        '''
        Set mode to Auto
        :param Nothing
        :return: Nothing
        '''
        #TODO: Verify and return new state
        self.msrc.set_mode_auto()

    def setManual(self):
        '''
        Set mode to Manual
        :param Nothing
        :return: Nothing
        '''
        #TODO: Verify and return new state
        self.msrc.setManual()

    def setRTL(self):
        '''
        Set mode to RTL
        :param Nothing
        :return: Nothing
        '''
        #TODO: Verify and return new state
        self.msrc.setRTL()

    def monitorThread(self):
        '''
        Thread responsible for collecting all incoming mavlink messages
        :param Nothing
        :return: Nothing
        '''
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
        #TODO: Write handlers for all packages, perhaps in a different class and extend it here
        if data._type is 'PARAM_VALUE':
            self.params[data.param_id.replace('\x00','')] = data.param_value


    def close(self):
        '''
        Cleanly terminates the monitor thread
        '''
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