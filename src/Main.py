from DirectoryTree import DirectoryTree
import unittest, os
from File import File
from Disks import Disks
from Utils import get_files_to_delete, get_human_readable_size

def get_files_by_level2(files):
    for f in files:
        print(f.get_file_info())
        print()

def get_readable_sizes(files):
    for f in files:
        print(get_human_readable_size(f))

if __name__ == '__main__':
    tree = DirectoryTree("~/Desktop/ml2018-19")
    files = tree.walklevel('~/Desktop/ml2018-19')
    #get_files_by_level2(gen)
    
    #tree.remove_tree_node("/home/damian/Downloads/4B.cpp")
    #tree.remove_directory("/home/damian/Downloads/sort")

    print("FILES TO REMOVE")
    number_files_to_remove = 5
    in_past = 20
    mode = 'days'
    files_to_remove = get_files_to_delete(tree.get_root(), number_files_to_remove, in_past, mode)
    get_files_by_level2(files_to_remove)
    get_readable_sizes(files_to_remove)

    d = Disks()
    print(d.get_partitions())
    d.disk_usage_for_partitions()

    for prt in d.get_partitions():
        print(prt)
