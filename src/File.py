import os, time

class File:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.file_type = os.path.isfile(path)
        self.time_creation = os.path.getctime(path)
        self.last_modified = os.path.getmtime(path)
        self.last_opened = os.path.getatime(path)
        self.file_size = os.path.getsize(path)
        #self.size_above = 10
    def __repr__(self):
        return "File {}, last access {} with size {} bytes".format(
            self.name, self.get_last_modified(), self.file_size
        )

    def convert_epoch_time_to_date(self, epoch_time):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))
    
    def get_file_info(self):
        return {
            "name": self.get_name(),
            "path": self.get_path(),
            "type": self.get_file_type(),
            "size": self.get_file_size(),
            "when_created": self.get_creation_time(),
            "last_modified": self.get_last_modified(),
            "last_access": self.get_last_opened()
        }

    def get_last_modified(self):
        return self.convert_epoch_time_to_date(self.last_modified)

    def get_creation_time(self):
        return self.convert_epoch_time_to_date(self.time_creation)

    def get_last_opened(self):
        return self.convert_epoch_time_to_date(self.last_opened)

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def get_file_type(self):
        return self.file_type

    def get_file_size(self):
        return self.file_size 
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