import os, sys
from os.path import expanduser
from File import File

class DirectoryTree:
    def __init__(self, path):
        self.path = expanduser(path) if path.startswith(("~", "/")) else path
        print(self.path)
        self.sizes_map = self.get_mapped_paths_with_sizes(self.get_parent(self.path))

    def get_size_directory_with_mapping(self, path, sizes_map):
        if self.file_to_skip(path):
            return 0

        if os.path.isfile(path) and not os.path.isdir(path):
            sizes_map[path] = os.path.getsize(path)
            return sizes_map[path]

        dir_entries = os.listdir(path)
        dir_size = 0
        for entry in dir_entries:
            next_path = os.path.abspath(os.path.join(path, entry))
            if os.path.isfile(next_path):
                dir_size += os.path.getsize(next_path)
            elif os.path.isdir(next_path):
                dir_size += self.get_size_directory_with_mapping(next_path, sizes_map)

        sizes_map[path] = dir_size
        return dir_size

    def get_mapped_paths_with_sizes(self, path):
        sizes_map = {}
        self.get_size_directory_with_mapping(path, sizes_map)
        return sizes_map

    def get_content_of_directory(self):
        if os.path.isfile(self.path):
            raise ValueError('{} is not a directory!'.
                format(self.path.split('\\')[-1]))

        return self.walklevel(depth=1)

    def get_recursive_content_of_directory(self):
        if os.path.isfile(self.path):
            raise ValueError('{} is not a directory!'.
                format(self.path.split('\\')[-1]))

        return self.walklevel(depth=-1)

    def check_access(self, path):
        return os.access(path, os.R_OK) and os.access(path, os.W_OK)

    def file_to_skip(self, path):
        return True if not self.check_access(path) or os.path.islink(path) else False

    def get_parent(self, path):
        return os.path.dirname(path) if os.path.isfile(path) else os.path.abspath(os.path.join(path, ".."))

    def get_file(self, path):
        parent_path = self.get_parent(path)
        f = File(path.split('/')[-1], path, self.sizes_map[path], self.sizes_map[parent_path])
        return f

    def walklevel(self, depth=1):
        abs_path = self.path
        if abs_path.startswith("~") or abs_path.startswith("/"):
            abs_path = os.path.expanduser(abs_path)

        if depth < 0:
            for root, dirs, files in os.walk(abs_path):
                if not self.file_to_skip(root):
                    yield self.get_file(root)

        abs_path = abs_path.rstrip(os.path.sep)
        num_sep = abs_path.count(os.path.sep)
        for root, dirs, files in os.walk(abs_path):
            if not self.file_to_skip(root):
                yield self.get_file(root)
            num_sep_this = root.count(os.path.sep)
            if num_sep + depth <= num_sep_this:
                del dirs[:]
        

    def walklevel_info_subdirs_and_files(self, depth=1):
        abs_path = self.path
        if abs_path.startswith("~") or abs_path.startswith("/"):
            abs_path = os.path.expanduser(abs_path)

        if depth < 0:
            for root, dirs, files in os.walk(abs_path):
                if not self.file_to_skip(root):
                    yield root, dirs, files
        
        abs_path = abs_path.rstrip(os.path.sep)
        num_sep = abs_path.count(os.path.sep)
        for root, dirs, files in os.walk(abs_path):
            if not self.file_to_skip(root):
                yield root, dirs, files
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + depth <= num_sep_this:
                del dirs[:]