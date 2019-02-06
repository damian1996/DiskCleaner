import os
import time


class File:
    def __init__(self, path):
        self.name = path.split('/')[-1] if path != '/' else '/'
        self.path = path
        self.is_file = os.path.isfile(path)
        self.size, self.parent_size = 0, 0
        self.next_files = []

    def __repr__(self):
        return "File {}".format(self.name)

    def get_file_info(self):
        files_count, count_subdirs = self.count_files_and_subdirs()
        return {
            "name": self.get_name(),
            "path": self.get_path(),
            "is_file": self.if_is_file(),
            "size": self.size,
            "creation_date": self.get_creation_date_in_seconds(),
            "last_modified": self.get_last_modified_date_in_seconds(),
            "last_access": self.get_last_opened_date_in_seconds(),
            "files_count": files_count,
            "subdirectiories_count": count_subdirs,
            "parent_directory_size": self.parent_size
        }

    def get_children(self):
        return self.next_files

    def set_size(self, size):
        self.size = size

    def set_parent_size(self, parent_size):
        self.parent_size = parent_size

    def add_next_child(self, file):
        self.next_files.append(file)

    def get_last_modified_date_in_seconds(self):
        return os.path.getmtime(self.path)

    def get_creation_date_in_seconds(self):
        return os.path.getctime(self.path)

    def get_last_opened_date_in_seconds(self):
        return os.path.getatime(self.path)

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def if_is_file(self):
        return self.is_file

    def get_size(self):
        return self.size

    def get_size_parent_directory(self):
        return self.parent_size

    def count_files_and_subdirs(self):
        if self.if_is_file():
            return 0, 0

        onlyfiles = sum(child.if_is_file() for child in self.next_files)
        return onlyfiles, len(self.next_files) - onlyfiles

    def decrease_sizes(self, to_decrease):
        self.size -= to_decrease
        self.parent_size -= to_decrease

    def delete_child(self, index):
        del self.next_files[index]
