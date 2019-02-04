import datetime, time, os
from copy import deepcopy

def convert_epoch_time_to_date(epoch_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))

def get_human_readable_size(node):
    next_boundaries = [(1e+3, 1, "B"), (1e+6, 1e+3, "kB"), (1e+9, 1e+6, "MB")]
    readable_size = node.get_size()
    for boundary, divider, unit in next_boundaries:
        if readable_size < boundary:
            return "{} {}".format(round(readable_size/divider, 2), unit)    
    return "{} {}".format(round(readable_size/1e+9, 2), "GB")

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

def get_files_fulfilling_condition(node, predicate, date_bound, curr_time, mode, all_files):
    last_modified_in_sec = node.get_last_modified_date_in_seconds()
    last_modified_time = datetime.datetime.utcfromtimestamp(last_modified_in_sec)
    if mode == 'days':
        last_modified_time = last_modified_time + datetime.timedelta(days=+date_bound)
    elif mode == 'months':
        last_modified_time = last_modified_time + relativedelta(months=+date_bound)
    
    if not node.if_is_file():
        for child in node.get_children():
            get_files_fulfilling_condition(child, predicate, date_bound, curr_time, mode, all_files)
    elif predicate(last_modified_time, curr_time):
        all_files.append(node)

def get_files_to_delete(root, number_files_to_remove, date_bound, mode):
    all_files = []
    curr_time = datetime.datetime.now()
    predicate = lambda node_time, curr_time: node_time < curr_time
    get_files_fulfilling_condition(root, predicate, date_bound, curr_time, mode, all_files)
    if len(all_files) < number_files_to_remove:
        return all_files
    else:
        files_sorted_by_size = sort_files_by_size(all_files, desc=True)
        return files_sorted_by_size[:number_files_to_remove]

def get_list_of_files_objects_older_than_date(node, predicate, bound_date, all_files):
    if node.if_is_file():
        last_modified_in_sec = node.get_last_modified_date_in_seconds()
        last_modified_time = datetime.datetime.utcfromtimestamp(last_modified_in_sec)
        if predicate(last_modified_time, bound_date):
            all_files.append(node)
            return True
        return False
    else:
        size_before = len(all_files)
        are_older = True
        for child in node.get_children():
            is_subdir_older = get_list_of_files_objects_older_than_date(child, predicate, bound_date, all_files)
            are_older = are_older and is_subdir_older
        if are_older:
            for i in range(size_before, len(all_files)):
                all_files.pop()
            all_files.append(node)
            return True
        return False

def get_files_and_dirs_to_delete(root, number_files_to_remove, date_bound, mode):
    all_files = []
    curr_time = datetime.datetime.now()
    if mode == 'days':
        bound_date = curr_time + datetime.timedelta(days=-date_bound)
    elif mode == 'months':
        bound_date = curr_time + relativedelta(months=-date_bound)
    predicate = lambda node_time, bound_date: node_time < bound_date

    get_list_of_files_objects_older_than_date(root, predicate, bound_date, all_files)
    if len(all_files) < number_files_to_remove:
        return all_files
    else:
        files_sorted_by_size = sort_files_by_size(all_files, desc=True)
        return files_sorted_by_size[:number_files_to_remove]