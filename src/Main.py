from DirectoryTree import DirectoryTree
import unittest, os
from File import File
from Disks import Disks

def get_files_by_level2(gen):
    while True:
        try:
            file = next(gen)
            print(file.get_file_info(), '\n')
        except StopIteration:
            print("The end. ")
            break

if __name__ == '__main__':
    tree = DirectoryTree("/home/damian")
    gen = tree.walklevel()
    get_files_by_level2(gen)
    '''
    d = Disks()
    print(d.get_partitions())
    d.disk_usage_for_partitions()

    gen = d.get_partitions()
    while True:
        try:
            partition = next(gen)
            print(partition)
        except StopIteration:
            break
    '''