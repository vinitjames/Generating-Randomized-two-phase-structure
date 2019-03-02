import numpy as np
import math

def dist_between_lines(a0,a1,b0,b1,clampAll=False,clampA0=False,clampA1=False,clampB0=False,clampB1=False):

    ''' Given two lines defined by numpy.array pairs (a0,a1,b0,b1)
        Return the closest points on each segment and their distance
    '''

    # If clampAll=True, set all clamps to True
    if clampAll:
        clampA0=True
        clampA1=True
        clampB0=True
        clampB1=True

    # Calculate denomitator
    A = a1 - a0
    B = b1 - b0
    magA = np.linalg.norm(A)
    magB = np.linalg.norm(B)

    _A = A / magA
    _B = B / magB

    cross = np.cross(_A, _B);
    denom = np.linalg.norm(cross)**2

    # If lines are parallel (denom=0) test if lines overlap.
    # If they don't overlap then there is a closest point solution.
    # If they do overlap, there are infinite closest positions, but there is a closest distance
    if not denom:
        d0 = np.dot(_A,(b0-a0))

        # Overlap only possible with clamping
        if clampA0 or clampA1 or clampB0 or clampB1:
            d1 = np.dot(_A,(b1-a0))

            # Is segment B before A?
            if d0 <= 0 >= d1:
                if clampA0 and clampB1:
                    if np.absolute(d0) < np.absolute(d1):
                        return a0,b0,np.linalg.norm(a0-b0)
                    return a0,b1,np.linalg.norm(a0-b1)


            # Is segment B after A?
            elif d0 >= magA <= d1:
                if clampA1 and clampB0:
                    if np.absolute(d0) < np.absolute(d1):
                        return a1,b0,np.linalg.norm(a1-b0)
                    return a1,b1,np.linalg.norm(a1-b1)


        # Segments overlap, return distance between parallel segments
        return None,None,np.linalg.norm(((d0*_A)+a0)-b0)

    # Lines criss-cross: Calculate the projected closest points
    t = (b0 - a0);
    detA = np.linalg.det([t, _B, cross])
    detB = np.linalg.det([t, _A, cross])

    t0 = detA/denom;
    t1 = detB/denom;

    pA = a0 + (_A * t0) # Projected closest point on segment A
    pB = b0 + (_B * t1) # Projected closest point on segment B


    # Clamp projections
    if clampA0 or clampA1 or clampB0 or clampB1:
        if clampA0 and t0 < 0:
            pA = a0
        elif clampA1 and t0 > magA:
            pA = a1

        if clampB0 and t1 < 0:
            pB = b0
        elif clampB1 and t1 > magB:
            pB = b1

        # Clamp projection A
        if (clampA0 and t0 < 0) or (clampA1 and t0 > magA):
            dot = np.dot(_B,(pA-b0))
            if clampB0 and dot < 0:
                dot = 0
            elif clampB1 and dot > magB:
                dot = magB
            pB = b0 + (_B * dot)

        # Clamp projection B
        if (clampB0 and t1 < 0) or (clampB1 and t1 > magB):
            dot = np.dot(_A,(pB-a0))
            if clampA0 and dot < 0:
                dot = 0
            elif clampA1 and dot > magA:
                dot = magA
            pA = a0 + (_A * dot)


    return None,None,np.linalg.norm(pA-pB)

def point_in_cylinder(point,vertice1, vertice2, radius):
    vec= vertice2 - vertice1
    const = radius* np.linalg.norm(vec)
    return (np.dot(point - vertice1, vec) >= 0 and
            np.dot(point - vertice2, vec) <= 0 and
            np.linalg.norm(np.cross(point - vertice1, vec)) <= const)

def distance_between_points(pt1,pt2):
    return np.linalg.norm(pt1-pt2)

def distance_from_plane(plane=None,point=None):
    ''' Given a plane defined by a numpy array of 3 points and a point also a single point
        the function calculates the distance of the point from the plane'''
   
    # Check if the point is in plane  
    v1= plane[0] - plane[1]
    v2= plane[2] - plane[1]
    normal = np.cross(v1,v2)
    normal=normal/np.linalg.norm(normal)
    tol=0.001
    dot_product=np.dot(point-plane[0],normal)
    #import ipdb;ipdb.set_trace()
    if abs(dot_product)<=tol:
        point_in_plane=True
    else:
        point_in_plane=False
        dist=dot_product
        
    if point_in_plane:
        p1=np.dot(plane[1]-point,plane[1]-plane[0])
        p2=np.dot(plane[1]-point,plane[2]-plane[1])
        l1=np.dot(plane[1]-plane[0],plane[1]-plane[0])
        l2=np.dot(plane[2]-plane[1],plane[2]-plane[1])
        if p1>0 and p1<l1 and p2>0 and p2< l2:
            dist=0
        else:
            d1=np.linalg.norm(plane[0]-point)
            d2=np.linalg.norm(plane[1]-point)
            d3=np.linalg.norm(plane[2]-point)
            d4=np.linalg.norm(plane[3]-point)
            dist=min(d1,d2,d3,d4)
            
    return dist

def rotation_matrix(dir=None,cos=0.0,sin=0.0):
    if dir in ['x','X']:
        return np.asarray([[1,0,0],[0,cos,sin],[0,-sin,cos]])
    if dir in ['y','Y']:
        return np.asarray([[cos,0,-sin],[0,1,0],[sin,0,cos]])
    if dir in ['z','Z']:
        return np.asarray([[cos,sin,0],[-sin,cos,0],[0,0,1]])

def get_rand_3dpoint(limit_dim=None,x_limit=None,y_limit=None,z_limit=None):
    if limit_dim is None:
        limit_dim=[x_limit,y_limit,z_limit]
    rand_x=np.random.uniform(low=-limit_dim[0],high=limit_dim[0])
    rand_y=np.random.uniform(low=-limit_dim[1],high=limit_dim[1])
    rand_z=np.random.uniform(low=-limit_dim[2],high=limit_dim[2])
    return np.asarray([rand_x,rand_y,rand_z])

if __name__=='__main__':
    plane=np.asarray([[0,0,0],[0,2,0],[2,0,0],[2,2,0]])
    point1=np.asarray([0.5,0.5,0])
    point2=np.asarray([0.5,-0.5,0])
    point3=np.asarray([-0.5,0.5,0])
    point4=np.asarray([-0.5,-0.5,0])
    print(dist_between_lines(point1,point2,point3,point4))
    print(distance_from_plane(plane,point1))
    print(rotation_matrix('z',0.5,0.4))
