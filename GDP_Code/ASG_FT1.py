import Queue			# for communicating between threads
import __main__
SoarQ = Queue.Queue(1) 	# this stores info on soaring
__main__.SoarQ = SoarQ

import PanicMode       # use to enter panic mode
import ArtSoar
import sys				# for exception handling
import threading

from ASG.TidyCode.inflight_run_script_v4 import LoopMainRun
import time

class SingleFunction(threading.Thread):
	def __init__(self,ID,function,kill):
		threading.Thread.__init__(self)
		self.ID = ID
		self.function = function
		self.kill = kill

	def run(self):
		try:
			self.function(self.kill)
		except PanicMode.PanicPanic, msg:
			print(msg)
			ExcQ.put(sys.exc_info())
			raise#return None
		except:
			print("Unrecognised failure")
			ExcQ.put(sys.exc_info())
			raise#return None
		print("SingleFunction ID%d ran successfully" %self.ID)
		pass

# Create queues to communicate exceptions between functions
ExcQ = Queue.Queue()		# function post here if they've failed

def Run1():
	Kill = [] 		# these are the queues that will help kill each thread
	Threads = []	# this is a list of all created threads
	
	# Create monitoring thread
	kMonitor = Queue.Queue(1)
	tMonitor = SingleFunction(1,PanicMode.VehicleMonitor,kMonitor)
	Kill.append(kMonitor)
	Threads.append(tMonitor)

	# Create worker thread
	kWorker = Queue.Queue(1)
	tWorker = SingleFunction(2,LoopMainRun,kWorker)
	Kill.append(kWorker)
	Threads.append(tWorker)

	# Create soaring thread
	kSoar = Queue.Queue(1)
	tSoar = SingleFunction(3,ArtSoar.Wait,kSoar)
	Kill.append(kSoar)
	Threads.append(tSoar)

	# soarQ gone

	# Start the threads
	for thread in Threads:
		thread.start()

	# Let it run whilst all is fine
	while ExcQ.empty():
		time.sleep(0.1)

	# Error detection
	print("Issue detected:\n%s" %str(ExcQ.get()))

	# Send message to kill everything
	for k in Kill:
		k.put(1)

	# Go into panic mode first
	PanicMode.Enter()
	# Ensure everything has stopped
	for t in Threads:
		print("Trying to kill: %s" %str(t.function))
		t.join()
	print("All killed, entering panic mode")
	# Redo panic mode just in case
	PanicMode.Enter()
	pass
