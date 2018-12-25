import os, time

class File:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.file_type = os.path.isfile(path)
        self.size, self.parent_size = 0, 0
        self.next_files = []

    def __repr__(self):
        return "File {}".format(self.name)

    def convert_epoch_time_to_date(self, epoch_time):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))
    
    def get_file_info(self):
        count_files, count_subdirs = self.count_files_and_subdirs()
        return {
            "name": self.get_name(),
            "path": self.get_path(),
            "type": self.get_file_type(),
            "size": self.size,
            "when_created": self.get_creation_time(),
            "last_modified": self.get_last_modified_time(),
            "last_access": self.get_last_opened_time(),
            "count_files": count_files,
            "count_subdirectories": count_subdirs,
            "size_parent_directory": self.parent_size,          
        }

    def get_children(self):
        return self.next_files

    def set_size(self, size):
        self.size = size

    def set_parent_size(self, parent_size):
        self.parent_size = parent_size

    def add_next_child(self, file):
        self.next_files.append(file)

    def get_last_modified_time(self):
        return self.convert_epoch_time_to_date(os.path.getmtime(self.path))

    def get_creation_time(self):
        return self.convert_epoch_time_to_date(os.path.getctime(self.path))

    def get_last_opened_time(self):
        return self.convert_epoch_time_to_date(os.path.getatime(self.path))

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def get_file_type(self):
        return self.file_type
    
    def get_size(self):
        return self.size

    def get_size_parent_directory(self):
        return self.parent_size

    def count_files_and_subdirs(self):
        if os.path.isfile(self.path):
            return 0, 0
        all_files_in_dir = len(os.listdir(self.path))
        onlyfiles = sum(os.path.isfile(os.path.join(self.path, f)) for f in os.listdir(self.path))
        return onlyfiles, all_files_in_dir - onlyfiles