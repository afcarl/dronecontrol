#In-flight energy balance
#Laurence Jackson, lj8g10
# 30/01/2015 read data from active_aircraft.py
#--------------------------------------------------------------------#
#
#where:     hA is current altitude
#           hB is next WP altitude
#           dAB is distance to next WP

from active_aircraft import * #!# aju
import ASG.ArtSoar
from __main__ import SoarQ

def inflight_stage(hA,hB,dAB,LD_ratio):

    delta_h_ideal = (1/LD_ratio)*dAB           #ideal altitude change from current position
                                            #to target WP based on ideal glide slope

    ideal_alt = hB + delta_h_ideal          #ideal altitude

    if hA < ideal_alt:

        delta_h_diff = ideal_alt - hA

        E_req_AB = m*g*delta_h_diff
        
        print ("More energy required!")
        print ("Additional alt required en route = %.3f m" % delta_h_diff)
        print ("Additional energy required en route = %.3f J" % E_req_AB)

        if hA+delta_h_diff < SF*hmax:

            print ("\nNow soaring %.3f m" % delta_h_diff)
	    SoarQ.put(delta_h_diff)

        elif hA+delta_h_diff > SF*hmax and hA > hmin:

            print ("\nSoaring now would exceed altitude ceiling")
            print ("Continuing on glide for now...")

        elif hA+delta_h_diff > SF*hmax and hA < hmin:

            print ("\nWARNING!! Dropping below minimum altitude!!")
            print ("Climbing to %.3f m altitude" % (SF*hmax))
	    SoarQ.put(SF*hmax-hA)
        
    else:

        E_req_AB = 0
        
        print ("No additional alt required to reach next WP")
        print ("No additional energy required to reach next WP")
        
#--------------------------------------------------------------------#



def flight_balance(z,d_WP,WP_target,N,h_route,d_route,LD_ratio):


    for i in range(N):
        if i+1 == WP_target and d_WP != 0:
            print ("You are at Stage %d: WP%d -> WP%d" %(i,i,i+1))
            print ("Distance to WP%d is %.3f m" %(i+1,d_WP))
            inflight_stage(z,h_route[i],d_WP,LD_ratio)
        elif i+1 == WP_target and d_WP == 0 and WP_target+1 < N+1:
            print ("You are at WP%d" %(WP_target))
            print ("Distance to WP%d is %.3f m" %(WP_target+1,d_route[i]))
        elif i+1 == WP_target and WP_target == N and d_WP == 0:
            print ("You are at final WP: WP%d" %(N))


