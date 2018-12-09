from DirectoryTree import DirectoryTree

if __name__ == '__main__':
    tree = DirectoryTree("..")
    #gen = tree.walklevel("~/Desktop", depth = 2)
    tree.get_files_by_level("~/Desktop", depth = 2)