__author__ = 'cpaulson'

from PyQt4 import QtCore, QtGui, uic
import sys, time
import copy

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = uic.loadUi('odroidButton.ui', self)
        self.ui.toolButton.clicked.connect(self.toggleOdroid)
        self.show()

    def toggleOdroid(self, state):
        if state:
            print 'Starting the ODroid'
        else:
            print 'Powering down the ODroid'


if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())