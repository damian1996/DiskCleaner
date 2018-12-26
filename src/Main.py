from DirectoryTree import DirectoryTree
import unittest, os
from File import File
from Disks import Disks

def get_files_by_level2(gen):
    for file in gen:
        print(file.get_file_info())

if __name__ == '__main__':
    tree = DirectoryTree("/home/damian/Downloads")
    gen = tree.walklevel('/home/damian/Downloads')
    get_files_by_level2(gen)
    #tree.remove_tree_node("/home/damian/Downloads/4B.cpp")
    #tree.remove_directory("/home/damian/Downloads/sort")
    d = Disks()
    print(d.get_partitions())
    d.disk_usage_for_partitions()

    for prt in d.get_partitions():
        print(prt)
