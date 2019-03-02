import numpy as np
import random
import math
from src.utils import utils


class Tube(object):
    
    def __init__(self,center=None,length=None,
                 dia=None,angle1=None,angle2=None):
        self.center = center
        self.length = length
        self.dia = dia
        self.angle1 = angle1
        self.angle2 = angle2
        self.vertice1 = None
        self.vertice2 = None
        self.create_tube()
        
    def create_tube(self):
        #initialize coordinates for vertices of the cylinder axis
        self.vertice1 = np.asarray([0, 0, self.length/2])
        self.vertice2 = np.asarray([0, 0, -self.length/2]) 
        #rotate the cylinder about x axis by alpha
        self.vertice1 = np.dot(utils.rotation_matrix('x', math.cos(math.radians(self.angle1)),
                                                     math.sin(math.radians(self.angle1))), self.vertice1)
        self.vertice2 = np.dot(utils.rotation_matrix('x', math.cos(math.radians(self.angle1)),
                                                     math.sin(math.radians(self.angle1))), self.vertice2)      
        #rotate the cylinder about y axis by beta
        self.vertice1 = np.dot(utils.rotation_matrix('y', math.cos(math.radians(self.angle2)),
                                                     math.sin(math.radians(self.angle2))), self.vertice1)
        self.vertice2 = np.dot(utils.rotation_matrix('y', math.cos(math.radians(self.angle2)),
                                                     math.sin(math.radians(self.angle2))), self.vertice2)
        #translating to Random point
        self.vertice1 += self.center
        self.vertice2 += self.center
        

class CNT(object):

    def __init__(self, config):
        self.vol = [float(dim) for dim in config['boundaryvolume']]
        self.limit_dim = np.asarray([self.vol[0]/2, self.vol[1]/2, self.vol[2]/2])
        self.tubelength = float(config['tubelength'][0])
        self.tubedia = float(config['tubediameter'][0])
        self.angleset = [float(dim) for dim in config['angleset']]
        self.no_of_tubes = int(config['tubecount'][0])
        self.tol = float(config['spacingtolerance'][0])
        self.tubes = []
        
    def check_dim_limit(self, points, limit_dim=None):
        if limit_dim is None:
            limit_dim = self.limit_dim
        for point in points:
            in_limit = (-limit_dim[0] < point[0] < limit_dim[0]
                        and -limit_dim[1] < point[1] < limit_dim[1]
                        and -limit_dim[2] < point[2] < limit_dim[2])
        return in_limit
        
    def create_struct(self):
        while len(self.tubes) < self.no_of_tubes:
            #generate random centre and angle for the tube
            rand_center = utils.get_rand_3dpoint(limit_dim=self.limit_dim-self.tubelength/2) 
            alpha,beta = random.sample(self.angleset,2)
            #create the tube with randomly generated data above 
            tube = Tube(center=rand_center, length=self.tubelength,
                        dia=self.tubedia, angle1=alpha, angle2=beta)
            #sanity check for the dimensions of the tubes
            if not self.check_dim_limit([tube.vertice1, tube.vertice2]):
                continue
            #check if the tube is not intersecting with all the other existing tubes
            if len(self.tubes) == 0:
                self.tubes.append(tube)
                print("no. of cnt created: ", len(self.tubes))
            else:
                for i, existing_tube in enumerate(self.tubes):
                    _, _, dist = utils.dist_between_lines(tube.vertice1, tube.vertice2,
                                                          existing_tube.vertice1, existing_tube.vertice2,
                                                          clampAll=True)
                    if dist < self.tubedia+self.tol:
                        break
                if i == len(self.tubes)-1:
                    self.tubes.append(tube)
                    print("no. of cnt created: ", len(self.tubes))


if __name__ == "__main__":
    pass

