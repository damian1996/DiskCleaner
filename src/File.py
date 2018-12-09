import os

class File:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.file_type = os.path.isfile(path)
        #self.when_created = os.path.isfile(path)
        self.last_modified = os.path.getctime(path)
        self.last_opened = os.path.getatime(path)
        self.file_size = os.path.getsize(path)
        #self.size_above = 10
    def __repr__(self):
        return "File {}, last access {} with size {}".format(
            self.name, self.last_modified, self.file_size
        )

    '''
    @property
    def last_modified(self):
        return self.last_modified
    
    @last_modified.setter
    def last_modified(self, date):
        self.last_modified = date

    def size_percents(self):
        return 100.0*(float(self.file_size)/float(self.size_above))
    '''