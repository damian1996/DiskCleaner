import os, sys, shutil
from os.path import expanduser
from File import File

class DirectoryTree:
    def __init__(self, path):
        self.path = expanduser(path) if path.startswith(("~", "/")) else path
        self.root, self.files = self.create_tree_with_computed_sizes(self.path)

    def create_tree_with_computed_sizes(self, path):
        files_dict = {}
        for dirname, subdirs, files in os.walk(path, topdown=False):
            root = File(dirname)
            dir_size = 0
            for entry in files:
                next_path = os.path.abspath(os.path.join(dirname, entry))
                if self.file_to_skip(next_path):
                    continue
                next_file = File(next_path)
                child_size = os.path.getsize(next_path)
                next_file.set_size(child_size)
                dir_size += child_size
                root.add_next_child(next_file)
                files_dict[next_path] = next_file

            for entry in subdirs:
                next_path = os.path.abspath(os.path.join(dirname, entry))
                if self.file_to_skip(next_path):
                    continue
                next_file = files_dict[next_path]
                dir_size += next_file.get_size()
                root.add_next_child(next_file)

            root.set_size(dir_size)
            for child in root.get_children():
                child.set_parent_size(dir_size)
            files_dict[dirname] = root
        
        files_dict[path].set_parent_size(0)
        return files_dict[path], files_dict

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
            yield child

    def remove_file(self, path):
        try:
            if not self.check_access(path):
                raise Exception('You have not access to {} or file does not exists'.format(path))
            file_to_remove = self.files[path]
            size_of_removed_file = file_to_remove.get_size()
            keys = self.files.keys()
            path_copy = str(path)
            while path_copy != '/':
                path_copy = os.path.abspath(os.path.join(path_copy, '..'))
                if not path_copy in keys:
                    break
                self.files[path_copy].decrease_sizes(size_of_removed_file)
            name = file_to_remove.get_name()
            parent_path = os.path.abspath(os.path.join(path, '..'))
            if parent_path in keys:
                parent_dir = self.files[parent_path]        
                for i, file in enumerate(parent_dir.get_children()):
                    if file.get_name() == name:
                        parent_dir.delete_child(i)
            os.remove(path)
        except KeyError:
            raise KeyError('File {} does not exists'.format(path.split('/')[-1]))
        except Exception as e:
            raise Exception(e)
        
    def remove_directory(self, dir_path):
        try:
            if not self.check_access(dir_path):
                raise Exception('You have not access to {} or directory does not exists'.format(dir_path))
            dir_to_remove = self.files[dir_path]
            size_of_removed_directory = dir_to_remove.get_size()
            keys = self.files.keys()
            path_copy = str(dir_path)
            while path_copy != '/':
                path_copy = os.path.abspath(os.path.join(path_copy, '..'))
                if not path_copy in keys:
                    break
                print(path_copy)
                self.files[path_copy].decrease_sizes(size_of_removed_directory)
            name = dir_to_remove.get_name()
            parent_path = os.path.abspath(os.path.join(dir_path, '..'))
            if parent_path in keys:
                parent_dir = self.files[parent_path]        
                for i, file in enumerate(parent_dir.get_children()):
                    if file.get_name() == name:
                        parent_dir.delete_child(i)
            shutil.rmtree(dir_path)
        except KeyError:
            raise KeyError('Directory {} does not exists'.format(dir_path.split('/')[-1]))
        except Exception as e:
            raise Exception(e)