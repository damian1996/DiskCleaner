from DirectoryTree import DirectoryTree

if __name__ == '__main__':
    tree = DirectoryTree("..")
    #gen = tree.walklevel("~/Desktop", depth = 2)
    tree.get_files_by_level("~/Desktop", depth = 2)
    '''
    while True:
        try:
            content = next(gen)
            if type(content[0]) is str: 
                dir_name, subdirs, files = content
                #print(dir_name)
                for f_name in files:
                    print(dir_name + f_name)
            elif type(content[0]) is list:
                subdirs, files = content
                print("Empty?")
        except StopIteration:
            print("The end.")
            break
    '''