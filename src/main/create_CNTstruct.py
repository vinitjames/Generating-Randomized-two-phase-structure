import numpy as np
import math
from  src.utils import utils
from src.data.database import Database
from src.structures.cnt import CNT
from src.utils import config_reader

if __name__ == '__main__':
    config = config_reader.read_config('config/CNT_config.dat')
    cnt = CNT(config) # create instance of CNT class 
    cnt.create_struct() # create structure of CNT
    aerogelread_filename = config['aerogeldatfile'][0]
    aerogelwrite_filename =  config['aerogeldatfile'][0].split('.')[0]+'result.dat'
    cntread_filename = config['cntdatfile'][0]
    cntwrite_filename = config['cntdatfile'][0]
    aerogelread_db = Database(aerogelread_filename)
    aerogel_reader = aerogelread_db.get_reader()
    aerogelwrite_db = Database(aerogelwrite_filename)
    aerogel_writer = aerogelwrite_db.get_writer()
    no_of_points_outside = 0
    no_of_points_removed = 0
    # Read aerogel file one row at a time and remove points which are enclosed with CNT 
    for row in aerogel_reader:
        for i, tube in enumerate(cnt.tubes):
            point = np.array([float(row[4]),float(row[5]),float(row[6])])
            if utils.point_in_cylinder(point,tube.vertice1,tube.vertice2,cnt.tubedia/2):
                break
        if i == len(cnt.tubes)-1:
            aerogel_writer.writerow(row)
            no_of_points_outside += 1
        else:
            no_of_points_removed += 1   
    print('no of points written:', no_of_points_outside)
    print('no of points removed:', no_of_points_removed)
    aerogelread_db.close()
    aerogelwrite_db.close()
    # create dat file for the cnt structure by reading the same cnt dat
    # file and altering the coordinates according to the cnt struct created
    for i,tube in enumerate(cnt.tubes):
        cntread_db = Database(cntread_filename)
        cnt_reader = cntread_db.get_reader()
        cntwrite_db = Database(cntwrite_filename.split('.')[0]+str(i)+'.dat')
        cntwriter = cntwrite_db.get_writer()
        for row in cnt_reader:
            point = np.array([float(row[4]),float(row[5]),float(row[6])])
            #first Rotation around x by tube angle 1
            point = np.dot(utils.rotation_matrix('x',math.cos(math.radians(tube.angle1)),
                                                 math.sin(math.radians(tube.angle1))),point)        
            #Second Rotation around y by tube angle 2
            point = np.dot(utils.rotation_matrix('y',math.cos(math.radians(tube.angle2)),
                                                 math.sin(math.radians(tube.angle2))),point)
            #translating to the center of tube
            point += tube.center
            row[4:7] = list(point)
            cntwriter.writerow(row)
        cntread_db.close()
        cntwrite_db.close()
