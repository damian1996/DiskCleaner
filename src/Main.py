from DirectoryTree import DirectoryTree
import unittest, os
from File import File
from Disks import Disks

def get_files_by_level(gen):
    while True:
        try:
            content = next(gen)
            if type(content[0]) is str: 
                dir_name, subdirs, files = content
                #print("DIRNAME is {}".format(dir_name))
                for f_name in files:
                    rel_path = dir_name + "/" + f_name
                    if rel_path.startswith(("~", "/")):
                        rel_path = os.path.expanduser(rel_path)
                    f = File(f_name, rel_path, 0, 0)
                    print(f.get_file_info())
                for subdir_name in subdirs:
                    rel_path = dir_name + "/" + subdir_name + "/"
                    if rel_path.startswith(("~", "/")):
                        rel_path = os.path.expanduser(rel_path)
                    f = File(subdir_name, rel_path, 0, 0)
                    print(f.get_file_info())
            elif type(content[0]) is list:
                subdirs, files = content
                print("Missing dir_name.")
        except StopIteration:
            print("The end.")
            break

def get_files_by_level2(gen):
    while True:
        try:
            file = next(gen)
            print(file.get_file_info())
        except StopIteration:
            print("The end.")
            break

if __name__ == '__main__':
    #tree = DirectoryTree("~/Documents")
    #gen = tree.walklevel(depth=1)
    #get_files_by_level2(gen)

    d = Disks()
    #print(d.get_partitions())
    #d.disk_usage_for_partitions()

    gen = d.get_partitions()
    while True:
        try:
            partition = next(gen)
            print(partition)
        except StopIteration:
            break