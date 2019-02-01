import os, sys, shutil
from os.path import expanduser
from File import File
from copy import deepcopy

class DirectoryTree:
    def __init__(self, path):
        self.path = expanduser(path) if path.startswith(("~", "/")) else path
        self.root, self.files = self.create_tree_with_computed_sizes(self.path)

    def get_root(self):
        return deepcopy(self.root)

    def traverse_files(self, root, dirname, files, storage_for_files):
        sum_sizes_of_files = 0
        for entry in files:
            next_path = os.path.abspath(os.path.join(dirname, entry))
            if self.is_file_to_skip(next_path):
                continue
            next_file = File(next_path)
            child_size = os.path.getsize(next_path)
            next_file.set_size(child_size)
            root.add_next_child(next_file)
            storage_for_files[next_file.get_path()] = next_file
            sum_sizes_of_files += next_file.get_size()
        return sum_sizes_of_files

    def traverse_subdirs(self, root, dirname, subdirs, storage_for_files):
        sum_sizes_of_subdirs = 0
        for entry in subdirs:
            next_path = os.path.abspath(os.path.join(dirname, entry))
            if self.is_file_to_skip(next_path):
                continue
            next_file = storage_for_files[next_path]
            sum_sizes_of_subdirs += next_file.get_size()
            root.add_next_child(next_file)
        return sum_sizes_of_subdirs

    def set_parent_size_for_children(self, root, dir_size):
        for child in root.get_children():
            child.set_parent_size(dir_size)

    def create_tree_with_computed_sizes(self, path):
        storage_for_files = {}
        for dirname, subdirs, files in os.walk(path, topdown=False):
            root = File(dirname)
            dir_size = 0
            dir_size += self.traverse_files(root, dirname, files, storage_for_files)
            dir_size += self.traverse_subdirs(root, dirname, subdirs, storage_for_files)
            self.set_parent_size_for_children(root, dir_size)
            root.set_size(dir_size)
            storage_for_files[dirname] = root
        
        storage_for_files[path].set_parent_size(0)
        return storage_for_files[path], storage_for_files

    def check_access(self, path):
        return os.access(path, os.R_OK)

    def is_file_to_skip(self, path):
        return not self.check_access(path) or os.path.islink(path)

    def walklevel(self, path=''):
        path = path or self.path
        if path.startswith(("~", "/")):
            path = os.path.expanduser(path)

        root = self.files[path]
        return root.get_children()

    def update_tree_upwards(self, path, keys, size_of_removed_node):
        path_copy = str(path)
        while path_copy != '/':
            path_copy = os.path.abspath(os.path.join(path_copy, '..'))
            if not path_copy in keys:
                break
            self.files[path_copy].decrease_sizes(size_of_removed_node) 

    def delete_node_from_children_of_parent(self, path, node_to_remove, keys):
        name = node_to_remove.get_name()
        parent_path = os.path.abspath(os.path.join(path, '..'))
        if parent_path in keys:
            parent_dir = self.files[parent_path]
            for i, file in enumerate(parent_dir.get_children()):
                if file.get_name() == name:
                    parent_dir.delete_child(i)

    def remove_tree_node(self, path):
        try:
            if not self.check_access(path):
                raise Exception('You don\'t have access to {} or file does not exists'.format(path))
            node_to_remove = self.files[path]
            size_of_removed_node = node_to_remove.get_size()
            keys = self.files.keys()
            self.update_tree_upwards(path, keys, size_of_removed_node)
            self.delete_node_from_children_of_parent(path, node_to_remove, keys)
            os.remove(path) if node_to_remove.if_is_file() else shutil.rmtree(path)
        except KeyError:
            raise KeyError('File {} does not exists'.format(path.split('/')[-1]))
        except Exception as e:
            raise Exception(e)