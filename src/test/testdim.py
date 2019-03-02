from database import Database
import numpy as np

if __name__ == '__main__':
    #import ipdb; ipdb.set_trace()
    graphene_db=Database()
    start_reading= True
    max_x=0.0
    max_y=0.0
    max_z=0.0
    min_x=0.0
    min_y=0.0
    min_z=0.0
    db_reader=graphene_db.get_reader('testresult3.dat')
    for row in db_reader:
        if start_reading and not (not row):
            point=np.asarray([float(row[2]),float(row[3]),float(row[4])]) 
            max_x=max(max_x,point[0])
            max_y=max(max_y,point[1])
            max_z=max(max_z,point[2])
            min_x=min(min_x,point[0])
            min_y=min(min_y,point[1])
            min_z=min(min_z,point[2])
            
    print('max dimensions',max_x,max_y,max_z)
    print('min dimensions',min_x,min_y,min_z)
    
