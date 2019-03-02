import csv


class Database():
    
    def __init__(self,path):
        self.path=path
        self.data=None

    def get_reader(self):
        self.data=open(self.path)
        rowreader=csv.reader(self.data,delimiter=' ')
        return rowreader
        
    def get_writer(self):
        self.data=open(self.path, 'w', newline='')
        rowwriter = csv.writer(self.data, delimiter=' ',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        return rowwriter

    def close(self):
        self.data.close()
              
if __name__ == '__main__':
    no_of_points_outside=0
    read_db=Database('datfiles/graphene_7,28.dat')
    write_db=Database('datfiles/test1.dat')
    db_reader=read_db.get_reader()
    db_writer=write_db.get_writer()
    for row in db_reader:
        if 'Atoms' in row:
            import ipdb; ipdb.set_trace()
    


        
    

