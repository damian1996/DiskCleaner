import os, sys
from os.path import expanduser
from File import File

class DirectoryTree:
    def __init__(self, path):
        self.path = expanduser(path) if path.startswith(("~", "/")) else path
        self.files = {}
        self.root = self.get_mapped_paths_with_sizes(self.get_parent(self.path))

    def get_size_directory_with_mapping(self, path, f):
        dir_entries = os.listdir(path)
        dir_size = 0
        for entry in dir_entries:
            next_path = os.path.abspath(os.path.join(path, entry))
            if self.file_to_skip(next_path):
                continue
            next_file = File(entry, next_path)
            if os.path.isfile(next_path):
                child_size = os.path.getsize(next_path)
                next_file.set_size(child_size)
                dir_size += child_size
            elif os.path.isdir(next_path):
                child_size = self.get_size_directory_with_mapping(next_path, next_file)                
                next_file.set_size(child_size)
                dir_size += child_size

            f.add_next_child(next_file)
            self.files[next_path] = next_file

        for subfile in f.get_children():
            subfile.set_parent_size(dir_size)
        
        return dir_size

    def get_mapped_paths_with_sizes(self, path):
        root = File(path.split('/')[-1], path)
        self.get_size_directory_with_mapping(path, root)
        root.set_parent_size(root.get_size()) if path == '/' and self.path == '/' else root.set_parent_size(0)
        self.files[path] = root
        return root

    def check_access(self, path):
        return os.access(path, os.R_OK)

    def file_to_skip(self, path):
        return not self.check_access(path) or os.path.islink(path)

    def get_parent(self, path):
        return os.path.dirname(path) if os.path.isfile(path) else os.path.abspath(os.path.join(path, ".."))

    def walklevel(self, path=''):
        path = path if path != '' else self.path
        if path.startswith(("~", "/")):
            path = os.path.expanduser(path)

        root = self.files[path]
        for child in root.get_children():
            print(child)
            yield child