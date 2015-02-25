__author__ = 'cpaulson'
from driver import MAV
import time


def wp_cb(x):
    if x.seq == 3:
        print 'Triggering'
    if x.seq == 4:
        print 'Terminating'
    else:
        pass

print 'Starting MAV'
mav = MAV()

#allow some time for startup
#TODO: turn startup wait into a function with checking
time.sleep(5)
mav.waypointCallback = wp_cb

while True:
    time.sleep(15)


# for i in range(5):
#     mav.setParam('THR_MAX', i*20.0)
#     time.sleep(5)
# print mav.params
#
# for entry in mav.messages:
#     print entry
#     print mav.messageKeys[entry], '\n\n'

mav.close()
print 'Here!'

