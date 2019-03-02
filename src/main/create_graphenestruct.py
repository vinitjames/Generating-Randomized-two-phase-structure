import numpy as np
import math
from src.utils import utils
from src.utils import config_reader
from src.data.database import Database
from src.structures.graphene import Graphene


if __name__ == '__main__':
    config = config_reader.read_config('config/graphene_config.dat')
    graphene=Graphene(config)
    graphene.create_struct()
    graphene_directory=config['graphenedatfile'][0]
    resultdb_filename=config['resultdatfile'][0]
    resultdb=Database(resultdb_filename)
    resultwriter=resultdb.get_writer()
    atom_no=1 #global atom counter
    # transform the graphene flakes and write allthe flakes in the result file
    for flake_type in graphene.flakes.keys():
        if float(graphene.flake_len[flake_type]) == int (graphene.flake_len[flake_type]):
            filename=graphene_directory+'/flake_{}.dat'.format(int(graphene.flake_len[flake_type]))
        else:
            filename=graphene_directory+'/flake_{}.dat'.format(graphene.flake_len[flake_type])
        flakedb=Database(filename)
        for flake in graphene.flakes[flake_type]:
            start_reading = False
            flake_reader = flakedb.get_reader()
            for row in flake_reader:
                if 'Atoms' in row:
                    start_reading = True
                    continue
                if start_reading and len(row)!=0:
                    point=np.asarray([float(row[2]),float(row[3]),float(row[4])])
                    #First Rotation around x by angle1
                    point = np.dot(utils.rotation_matrix('x',math.cos(math.radians(flake.angle1)),
                                                         math.sin(math.radians(flake.angle1))),point)        
                    #Second Rotation around y by angle 2
                    point = np.dot(utils.rotation_matrix('y',math.cos(math.radians(flake.angle2)),
                                                         math.sin(math.radians(flake.angle2))),point)
                    #shift point to flakecentre 
                    point+=flake.center
                    row[0]=atom_no
                    row[2:5]=point
                    resultwriter.writerow(row[:5])
                    atom_no+=1
    #write the void centers in the result dat file                
    for void in graphene.voids:
        row = []
        row.append(atom_no)
        row.append(2) # atom type
        row.extend(void.center)
        resultwriter.writerow(row)
        atom_no += 1    
