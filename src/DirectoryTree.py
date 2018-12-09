import os, sys
from os.path import expanduser
from File import File

class DirectoryTree:
    def __init__(self, path):
        self.path = expanduser(path) if path in ["~","/"] else path

    def walklevel(self, path, depth = 1):
        """It works just like os.walk, but you can pass it a level parameter
        that indicates how deep the recursion will go.
        If depth is -1 (or less than 0), the full depth is walked.
        """
        if path.startswith("~") or path.startswith("/"):
            path = os.path.expanduser(path)

        if depth < 0:
            for root, dirs, files in os.walk(path):
                yield root, dirs, files
        
        path = path.rstrip(os.path.sep)
        num_sep = path.count(os.path.sep)
        for root, dirs, files in os.walk(path):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + depth <= num_sep_this:
                del dirs[:]
    
    def get_files_by_level(self, path, depth = 1):
        gen = self.walklevel(path, depth)
        while True:
            try:
                content = next(gen)
                if type(content[0]) is str: 
                    dir_name, subdirs, files = content
                    for f_name in files:
                        rel_path = dir_name + "/" + f_name
                        if rel_path.startswith(("~", "/")):
                            rel_path = os.path.expanduser(rel_path)
                        f = File(f_name, rel_path)
                        print(f)
                elif type(content[0]) is list:
                    subdirs, files = content
                    print("Missing dir_name.")
            except StopIteration:
                print("The end.")
                break
        
'''
if len(sys.argv) == 2:
    path = sys.argv[1] 

home = expanduser("~")

files = os.listdir(home)
no_hidden = list(filter(lambda x: not str(x).startswith("."), files)) 
only_hidden = list(filter(lambda x: str(x).startswith("."), files)) 
'''