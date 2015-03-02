#One script to rule them all...
#Laurence Jackson, lj8g10
# 30/01/2015 import data from active_aircraft.py

import math
import time
from inflight_balance_calculation_v5 import inflight_stage,flight_balance
from coord_WP_dist import get_coords,WP_dist
from wind_consideration_v2 import Opt_LD

"""UAV/glider flight parameters"""
from active_aircraft import m    # UAV/glider mass
from active_aircraft import g    # gravitational constant
from active_aircraft import hmax # Max flight ceiling
from active_aircraft import hmin # Min safe flight altitude
from active_aircraft import SF   # Safety factor
from active_aircraft import A    #V^2 coeff
from active_aircraft import B    #V coeff
from active_aircraft import C    #Constant
# Above could be acheived by "from active_aircraft import *" but didn't do it for clarity

from __main__ import v
cmds = v.commands

coords = get_coords("/home/andy/ardupilot/ArduPlane/ASG_WP.txt")

def LoopMainRun(alert,t=1):
	while alert.empty():
		start = time.time()
		MainRun()
		wait = t - (time.time()-start)
		if wait>0:
			time.sleep(wait)
	print("LoopMainRun detected an alarm, terminating")

def MainRun():

    """Flight Route input by pilot"""

    h_route,d_route = WP_dist(coords)

    N = len(h_route)


    #----------------------------------------------------------------------#

    # Values Read from the UAV autopilot while flying #

    Vs = 0                        #vertical air mass velocity, +ve defined as rising air mass
    Vw =  0                       #wind velocity component parallel to flight direction, +ve defined as head wind
    z = v.location.alt                         #current altitude                   
    WP_target = cmds.next                 #next waypoint reference number
	
    print(WP_target)
    print(cmds)
    currentLoc = [v.location.lat,v.location.lon,z]
    #nextWP = cmds[WP_target]
    nextLoc = coords[WP_target] #[nextWP.x, nextWP.y, nextWP.z]

    d_WP = WP_dist([currentLoc,nextLoc])[1][0]                      #distance to next waypoint

    #----------------------------------------------------------------------#

    # Flight Balance is calculated #

    LD_ratio = Opt_LD(Vw,Vs,A,B,C)

    flight_balance(z,d_WP,WP_target,N,h_route,d_route,LD_ratio)

    pass #end main run
