# Import necessary modules
from droneapi.lib import VehicleMode

# Assume we are already connected to a vehicle (at the highest
#  level) and this has been assigned to __main__.v
from __main__ import v

def FetchParam(par):
	global v
	"""
	Take a list of parameters (par) and returns a corresponding
	list of values from the vehicle."""
	v.flush() 		# just an extra one for luck
	val = par[:]	# create list for values
	for (i,p_) in enumerate(par):
		if p_=='MODE':
			# Treat modes slightly differently
			val[i] = v.mode.name
		else: val[i] = v.parameters[p_]

	return val

def SetMode(mode):
	global v
	"""
	Sets a new mode for the vehicle (e.g. MANUAL, AUTO, RTL).
	Function returns nothing."""
	v.mode = VehicleMode(mode)
	
	# Assumed that v.flush is run SetParam()
	#v.flush()
	pass

def SetParam(par,val):
	global v
	"""
	Sets a list of parameters (par) to a corresponding list of
	new values (val). Function returns nothing."""

	for (p_,v_) in zip(par,val):
		if p_=='MODE':
			# Treat modes slightly differently
			SetMode(v_)
		else:
			v.parameters[p_] = v_
	v.flush() 	# param changes SHOULD be guaranteed from now
	pass

def ChangeParam(par,val,checks=3):
	"""
	Change a list of parameters (par) to a corresponing list
	of new values (val). The parameter is then checked to
	ensure it has changed using CheckParam().

	Function returns 'True' if successful, otherwise returns
	a list of unset parameters."""
	SetParam(par,val)

	check = CheckParam(par,val)
	ci=0
	while (check!=True) and (ci<checks):
		ci+=1
		v.flush()
		check = CheckParam(check[0],check[1])
	if check!=True:
		print("Detected non-matching params: %s" %check[0]) 
		return check
	return True 

def CheckParam(par,val):
	"""
	Checks a list of parameters (par) are set to a list of
	values (val)."""
	valC = FetchParam(par)	# load Current parameter values
	parW = []				# list of params not correct
	valW = []				# list of values to be corrected

	# Iterate through each parameter, checking they have been
	#  changed correctly.
	for (p_,v_,vC_) in zip(par,val,valC):
		if p_!='MODE' and v_!=vC_: # skips mode changes
			parW.append(p_)
			valW.append(v_)
	
	# Return unchanged params or True
	if len(parW) > 0:
                return [parW, valW]
	return True 	# Everything okay
