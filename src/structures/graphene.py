import random
import numpy as np
import math
from src.utils import utils
from src.utils import config_reader


class Void(object):
    
    def __init__(self,center=None,dia=None):
        self.center = center
        self.dia = dia
        
    def create_void(self):
        # complex attributes of voids can be added here
        pass  

    
class Flake(object):
    
    def __init__(self,center=None,length=None,angle1=None,angle2=None,vol_type='sphere'):
        self.center = center
        self.length = length
        self.vol_type = vol_type
        self.angle1 = angle1
        self.angle2 = angle2
        
    def create_flake(self):
        #for adding complex attributes to the flake
        pass

    
class Graphene(object):

    def __init__(self,config):
        self.vol = [float(dim) for dim in config['boundaryvolume']]
        self.limit_dim = np.asarray([self.vol[0]/2,self.vol[1]/2,self.vol[2]/2]) 
        self.flake_len = {key:float(config[key][0]) for key in config.keys() if 'type' in key}
        self.no_flakes = {key:float(config[key][1]) for key in config.keys() if 'type' in key}
        self.tol = float(config['spacingtolerance'][0])
        self.angle_set = [float(dim) for dim in config['angleset']]
        self.no_of_voids = int(config['inclusioncount'][0])
        self.void_dia = float(config['inclusiondiameter'][0])
        self.voids = []
        self.flakes = {}
        self.flake_count = 0
        
    def check_interflake_intersection(self, flake):
        flake_intersect = False
        for existing_flake_type in self.flakes.keys():
            if len(self.flakes[existing_flake_type]) == 0:
                continue
            existing_len = self.flakes[existing_flake_type][0].length
            dist_allowed = (flake.length + existing_len)/math.sqrt(2)
            for existing_flake in self.flakes[existing_flake_type]:
                dist = utils.distance_between_points(existing_flake.center, flake.center)
                if dist < (dist_allowed + self.tol) :
                    flake_intersect = True
                    break
            if flake_intersect:
                break
        return flake_intersect
        
    def check_flakevoid_intersection(self, flake):
        flake_intersect = False
        for void in self.voids:
            dist = utils.distance_between_points(flake.center, void.center)
            if dist < (flake.length*math.sqrt(2)+void.dia)/2 + self.tol:
                flake_intersect = True
                break
        return flake_intersect
    
    def check_voidflake_intersection(self, void):
        void_intersect = False
        for existing_flake_type in self.flakes.keys():
            if len(self.flakes[existing_flake_type]) == 0:
                continue
            existing_len = self.flakes[existing_flake_type][0].length
            dist_allowed = (void.dia + existing_len*math.sqrt(2))/2
            for existing_flake in self.flakes[existing_flake_type]:
                dist = utils.distance_between_points(existing_flake.center, void.center)
                if dist < (dist_allowed + self.tol) :
                    void_intersect = True
                    break
            if void_intersect:
                break
        return void_intersect

    def check_intervoid_intersection(self, void):
        void_intersect = False
        for existing_void in self.voids:
            dist = utils.distance_between_points(existing_void.center, void.center)
            if dist < (existing_void.dia+void.dia)/2:
                void_intersect = True
                break
        return void_intersect
        
    def create_flakes(self, no_of_flakes=None, flake_type=None):
        flake_len = self.flake_len[flake_type]
        if flake_type not in self.flakes.keys():
            self.flakes[flake_type] = []
        while len(self.flakes[flake_type]) < no_of_flakes:
            pt_center = utils.get_rand_3dpoint(limit_dim=self.limit_dim-flake_len/2)
            alpha, beta = random.sample(self.angle_set, 2)
            flake = Flake(center=pt_center, length=flake_len, angle1=alpha, angle2=beta)
            if self.flake_count == 0  and len(self.voids) == 0:
                self.flakes[flake_type].append(flake)
                self.flake_count += 1
            else:
                if not self.check_interflake_intersection(flake):
                    if not self.check_flakevoid_intersection(flake):
                        self.flakes[flake_type].append(flake)
                        self.flake_count += 1
                        print('No. of voids and flakes: ', self.flake_count+len(self.voids))
                            
    def create_voids(self, no_of_voids=None,void_dia=None):
        while len(self.voids) < no_of_voids:
            pt_center = utils.get_rand_3dpoint(limit_dim=self.limit_dim-void_dia/2)
            void=Void(center=pt_center,dia=void_dia)
            if self.flake_count == 0 and len(self.voids)==0:
                self.voids.append(void)
            else:
                if not self.check_intervoid_intersection(void):
                    if not self.check_voidflake_intersection(void):
                        self.voids.append(void)
                        print('No. of voids and flakes: ', self.flake_count+len(self.voids))
                        
    def create_struct(self):
        #create voids
        self.create_voids(no_of_voids=self.no_of_voids,void_dia=self.void_dia)
        # create graphene flakes
        for flake_type in self.flake_len.keys():
            self.create_flakes(no_of_flakes=self.no_flakes[flake_type],flake_type=flake_type)

            
if __name__ == '__main__':
    print('testresult')
    config = config_reader.read_config('graphene_config.txt')
    graphene=Graphene(config)
    import ipdb; ipdb.set_trace()
