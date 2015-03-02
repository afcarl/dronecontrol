from math import radians, cos, sin, asin, sqrt

def get_coords(filename):
    """This function reads an input file in a standard APM/Mission Planner 2.0 format and exports them as a list of waypoints in a coordinate list with each element in format [latitude, longitude, altitude]."""
    coords=[]
    
    f=open(filename) #reading file
    text=f.read()
    f.close()
    lines=text.split('\n')[1:] #only reading data, not header

    for line in lines: #1 line at at time
        data=line.split()

        if len(data)>=11: #avoid header again and one test for invalid data
            lat=float(data[8])      #select appropriate data
            lon=float(data[9])
            alt=float(data[10])

            temp_coord=[lat,lon,alt]
            coords.append(temp_coord)
        else:
            break

    return coords

def WP_dist(coords):
    """This function uses the Haversine Formula [1, accessed 2014, Nov 4th, 20:45] to compute distances between a series of waypoints. input 'coords' is a list with minimum two elements in format [latitude, longitude, altitude]. Output in form [distance(WP1,WP2), altitude(WP1)]. Altitude is assumed to have little affect and it is not included in calculation."""
    #source1: http://en.wikipedia.org/wiki/Haversine_formula
    R_E=6371e3 #Earth's Radius in meters [2, google]
    
    def haversin(theta):
        """subfunction for special trig formula."""
        hsin=(1-cos(theta))/2.0
        return hsin
    def dist(lat1, lat2, lon1, lon2):
        """subfunction for calculating distance between two points using Haversine Formula referenced above."""
        d=2*R_E*asin(sqrt(haversin(lat2-lat1) +cos(lat1)*cos(lat2)*haversin(lon2-lon1)))
        return d

    out_dist=[]
    out_alt=[]
    for i in range(len(coords)):
        if (i+1)==len(coords):
            falt=coords[i][-1]
            fdist=0

            out_dist.append(0)
            out_alt.append(falt)
            break #last pair to calculate distance
        else:
            [lat1, lon1, alt1]=coords[i]
            [lat2, lon2, alt2]=coords[i+1]
            lat1, lon1, lat2, lon2=map(radians,[lat1, lon1, lat2, lon2]) #convert to radians for trig functions
            temp_dist=dist(lat1, lat2, lon1, lon2)

            #out_dist.append([temp_dist,(alt1, alt2)])
            out_alt.append(alt1)
            out_dist.append(temp_dist)
    return out_alt,out_dist
        
