#Laurence Jackson, lj8g10

#Wind consideration code:

import math

#This code uses the glide polar for the UAV (obtained through
#wind tunnel testing) to calculate optimal L/D ratio accounting
#for the effects of head/tailwinds and sink/rising air mass.

#The solutions/equations used below were obtained analytically.

#Note: positive Vw is defined as a headwind
#      positive Vs is defined as a rising air mass

def Opt_LD(Vw,Vs,A,B,C):         #optimal L/D is calculated as a function of wind velocity

    ##A,B,C are the glide polar Coefficients (quadratic relation)##

    V = ((2.*A*Vw)+ math.sqrt(((2.*A*Vw)**2.)+(4.*A*((B*Vw)+C-Vs))))/(2.*A)  #airspeed (at optimal L/D)

    Vv = (A*(V**2.))+(B*V)+C                 #sink rate (at optimal L/D)

    grad = (Vv-Vs)/(V-Vw)                 #gradient of tangent line (= L/D optimal)

    LD_opt = grad

    return LD_opt

#Optimal L/D is output, V is the required airspeed to achieve this optimal L/D




    
