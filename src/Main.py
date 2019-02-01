from DirectoryTree import DirectoryTree
import unittest, os
from File import File
from Disks import Disks
from Utils import get_files_to_remove, get_directories_to_remove

def get_files_by_level2(gen):
    for file in gen:
        print(file.get_file_info())
    print()

if __name__ == '__main__':
    tree = DirectoryTree("~/Desktop/ml2018-19")
    gen = tree.walklevel('~/Desktop/ml2018-19')
    get_files_by_level2(gen)
    #tree.remove_tree_node("/home/damian/Downloads/4B.cpp")
    #tree.remove_directory("/home/damian/Downloads/sort")
    files_to_remove = get_files_to_remove(tree.get_root())
    print("FILES TO REMOVE")
    get_files_by_level2(files_to_remove)

    dirs_to_remove = get_directories_to_remove(tree.get_root())
    print("DIRS TO REMOVE")
    get_files_by_level2(dirs_to_remove)

    d = Disks()
    print(d.get_partitions())
    d.disk_usage_for_partitions()

    for prt in d.get_partitions():
        print(prt)
