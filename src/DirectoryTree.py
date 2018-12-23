import os, sys
from os.path import expanduser
from File import File

class DirectoryTree:
    def __init__(self, path):
        self.path = expanduser(path) if path in ["~","/"] else path

    def get_content_of_directory(self, abs_path):
        if os.path.isfile(abs_path):
            raise ValueError('{} is not a directory!'.
                format(abs_path.split('\\')[-1]))

        return self.walklevel(abs_path, depth=1)

    def get_recursive_content_of_directory(self, abs_path):
        if os.path.isfile(abs_path):
            raise ValueError('{} is not a directory!'.
                format(abs_path.split('\\')[-1]))

        return self.walklevel(abs_path, depth=-1)

    def get_all_files_in_system(self):
        return self.walklevel("/", depth=-1)

    def walklevel(self, abs_path, depth=1):
        """
        It works just like os.walk, but you can pass it a level parameter
        that indicates how deep the recursion will go.
        If depth is -1 (or less than 0), the full depth is walked.
        """
        if abs_path.startswith("~") or abs_path.startswith("/"):
            abs_path = os.path.expanduser(abs_path)

        if depth < 0:
            for root, dirs, files in os.walk(abs_path):
                yield root, dirs, files
        
        abs_path = abs_path.rstrip(os.path.sep)
        num_sep = abs_path.count(os.path.sep)
        for root, dirs, files in os.walk(abs_path):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + depth <= num_sep_this:
                del dirs[:]