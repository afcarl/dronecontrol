__author__ = 'cpaulson'

from PyQt4 import QtCore, QtGui, uic
import sys, time
import copy
from pymavlink import mavutil


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.msrc = mavutil.mavlink_connection('udp:localhost:14552', planner_format=True, notimestamps=True,robust_parsing=True)
        self.msrc.wait_heartbeat()
        self.ui = uic.loadUi('odroidButton.ui', self)
        self.ui.toolButton.clicked.connect(self.toggleOdroid)
        self.show()

    def toggleOdroid(self, state):
        if state:
            print 'Starting the ODroid'
            self.msrc.set_relay(relay_pin=1, state=False)
        else:
            print 'Powering down the ODroid'
            self.msrc.set_relay(relay_pin=1, state=True)


if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())