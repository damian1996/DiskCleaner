import datetime, time, os
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

def get_files_fulfilling_condition(node, predicate, date_bound, curr_time, mode, all_files):
    last_opened_in_sec = node.get_last_opened_date_in_seconds()
    last_opened_time = datetime.datetime.utcfromtimestamp(last_opened_in_sec)
    if mode == 'days':
        last_opened_time = last_opened_time + datetime.timedelta(days=+date_bound)
    elif mode == 'month':
        last_opened_time = last_opened_time + relativedelta(months=+date_bound)
    
    if not node.if_is_file():
        for child in node.get_children():
            get_files_fulfilling_condition(child, predicate, date_bound, curr_time, mode, all_files)
    elif predicate(last_opened_time, curr_time):
        all_files.append(node)

def get_files_to_delete(root, number_files_to_remove, date_bound, mode):
    all_files = []
    curr_time = datetime.datetime.now()
    predicate = lambda node_time, curr_time: node_time > curr_time
    get_files_fulfilling_condition(root, predicate, date_bound, curr_time, mode, all_files)
    if len(all_files) < number_files_to_remove:
        return all_files
    else:
        files_sorted_by_size = sort_files_by_size(all_files, desc=True)
        return files_sorted_by_size[:number_files_to_remove]
