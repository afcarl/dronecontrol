from ArduParam import * # use FetchParam and ChangeParam
from __main__ import v
import time

# Define an exception that specifically requests panic mode
class PanicPanic(Exception):pass

# A function to enter panic mode
def Enter():
	# First change the mode to RTL
	ChangeParam(['MODE'],['RTL'])

	# Reinstate orginal parameters
	# ???
	print("EnterPanicMode complete")
	pass

# Check the current state, do we need to invoke a panic?
def Check(pL=40,pL_=-30,rL=65,vzL_=-20,aL=5): #correct PL_!!
	# Get current vehicle data
	p = v.attitude.pitch
	vz= v.velocity[2]
	r = abs(v.attitude.roll)	# use absolute value
	a = v.location.alt

	AttNames = ['pitch (+ve)','pitch -ve','roll','velocity (z)','altitude']
	AttCurrent = [p,-p,r,-vz,-a]
	AttLimit = [pL,-pL_,rL,-vzL_,-aL]

	for (name,cur,lim) in zip(AttNames,AttCurrent,AttLimit):
		if cur>lim:
			raise PanicPanic, "Outside operation: %s=%.2f" %(name,cur)
	print("Panic check is all okay") 	# may supress this
	pass

def VehicleMonitor(alert,t=0.5):
	while alert.empty():
		zero = time.time()
		Check()
		wait = t - (time.time() - zero)
		if wait>0:
			time.sleep(wait)
	print("VehicleMonitor detected alert, terminating")
	pass
