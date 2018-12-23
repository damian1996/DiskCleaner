import os, time

class File:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.file_type = os.path.isfile(path) # os.path.islink(path)

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
            "size": self.get_file_size(self.path),
            "when_created": self.get_creation_time(),
            "last_modified": self.get_last_modified_time(),
            "last_access": self.get_last_opened_time(),
            "count_files": count_files,
            "count_subdirectories": count_subdirs,
            "size_parent_directory": self.get_size_parent_directory(self.path),
        }

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

    def count_files_and_subdirs(self):
        if os.path.isfile(self.path):
            return 0, 0
        all_files_in_dir = len(os.listdir(self.path))
        onlyfiles = sum(os.path.isfile(os.path.join(self.path, f)) for f in os.listdir(self.path))
        return onlyfiles, all_files_in_dir - onlyfiles
        
    def get_file_size(self, path):
        if os.path.isfile(path) or not os.path.isdir(path):
            return os.path.getsize(path)
        return self.get_size_directory(path)

    def get_size_parent_directory(self, file):
        if self.file_type:
            dir_name = os.path.dirname(file)
            return self.get_size_directory(dir_name)
        abs_path = os.path.abspath(os.path.join(file, ".."))
        print(abs_path)
        return self.get_size_directory(abs_path)
    
    def get_size_directory(self, path):
        if os.path.isfile(path):
            return os.path.getsize(path)
        dir_entries = os.listdir(path)
        dir_size = 0
        for entry in dir_entries:
            next_path = os.path.abspath(os.path.join(path, entry))
            if os.path.isfile(next_path):
                dir_size += os.path.getsize(next_path)
            else:
                dir_size += self.get_size_directory(next_path)        
        return dir_size
