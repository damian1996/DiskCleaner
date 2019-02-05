from DirectoryTree import DirectoryTree
import unittest, os
from File import File
from Disks import Disks
from Utils import get_files_and_dirs_to_delete, get_human_readable_size
from dateutil.relativedelta import relativedelta

def get_files_by_level2(files):
    for f in files:
        print(f.get_file_info())
        print()

def get_readable_sizes(files):
    for f in files:
        print(get_human_readable_size(f))

if __name__ == '__main__':
    #"~/Desktop/Semestr7/ELMo-Implementation"
    tree = DirectoryTree("~/Downloads/projekt_angeli_na_ip/cuddly-octo-enigma/src")# "~/Desktop/ml2018-19")
    files = tree.walklevel("~/Downloads/projekt_angeli_na_ip/cuddly-octo-enigma/src") #('~/Desktop/ml2018-19')
    #get_files_by_level2(gen)
    
    #tree.remove_tree_node("/home/damian/Downloads/4B.cpp")
    #tree.remove_directory("/home/damian/Downloads/sort")

    #tree.remove_tree_nodes(files)

    print("FILES TO REMOVE")
    number_files_to_remove = 5
    in_past = 13
    sec = relativedelta(days=-in_past)

    files_and_dirs_to_remove = get_files_and_dirs_to_delete(tree.get_root(), number_files_to_remove, sec)
    print(files_and_dirs_to_remove)
    get_files_by_level2(files_and_dirs_to_remove)
    get_readable_sizes(files_and_dirs_to_remove)

    tree.remove_tree_nodes(files_and_dirs_to_remove)

    files_and_dirs_to_remove = get_files_and_dirs_to_delete(tree.get_root(), number_files_to_remove, sec)
    print(files_and_dirs_to_remove)
    get_files_by_level2(files_and_dirs_to_remove)
    get_readable_sizes(files_and_dirs_to_remove)

    d = Disks()
    print(d.get_partitions())
    d.disk_usage_for_partitions()

    for prt in d.get_partitions():
        print(prt)
