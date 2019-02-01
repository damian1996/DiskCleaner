import time, os
from copy import deepcopy

def convert_epoch_time_to_date(epoch_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))

def sort_files_by_opening_date(files, desc=False):
    f = lambda x: x.get_last_opened_date_in_seconds()
    files_to_sort = deepcopy(files)
    files_to_sort.sort(key=f, reverse=desc)
    return files_to_sort

def sort_files_by_modifing_date(files, desc=False):
    f = lambda x: x.get_last_modified_date_in_seconds()
    files_to_sort = deepcopy(files)
    files_to_sort.sort(key=f, reverse=desc)
    return files_to_sort

def sort_files_by_size(files, desc=False):
    f = lambda x: x.get_size()
    files_to_sort = deepcopy(files)
    files_to_sort.sort(key=f, reverse=desc)
    return files_to_sort

def get_propositions_to_remove(files, no_oldest, no_largest):
    sorted_files_by_date = sort_files_by_opening_date(files=files, desc=True)
    oldest_files = sorted_files_by_date[:no_oldest]
    sorted_files_by_size = sort_files_by_size(files=oldest_files, desc=True)
    return sorted_files_by_size[:no_largest]

def files_filtering(files, is_file):
    return [f for f in files if f.is_file == is_file]

def get_all_files_from_tree(node, all_files):
    all_files.append(node)
    for child in node.get_children():
        get_all_files_from_tree(child, all_files)

def get_files_to_remove(root):
    all_files = []
    get_all_files_from_tree(root, all_files)
    only_files = files_filtering(all_files, is_file=True)
    no_oldest = len(only_files) // 5
    no_largest = no_oldest // 3
    return get_propositions_to_remove(only_files, no_oldest, no_largest)

def get_directories_to_remove(root):
    all_files = []
    get_all_files_from_tree(root, all_files)
    only_dirs = files_filtering(all_files, is_file=False)
    no_oldest = len(only_dirs) // 5
    no_largest = no_oldest // 3
    return get_propositions_to_remove(only_dirs, no_oldest, no_largest)
