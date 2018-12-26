import psutil as ps

class Partition:
    def __init__(self, partition_info, partition_usage):
        self.device = partition_info.device
        self.mountpoint = partition_info.mountpoint
        self.total = partition_usage.total
        self.used = partition_usage.used
        self.free = partition_usage.free
        self.percents_usage = partition_usage.percent
    
    def __repr__(self):
        return 'Device {}, mounted at {}. Used memory is {}% of {} bytes' \
            .format(self.device, self.mountpoint, self.percents_usage, self.total)

    def get_name(self):
        return self.device

    def get_mountpoint(self):
        return self.mountpoint

    def get_total_size(self):
        return self.total
    
    def get_free_memory(self):
        return self.free

    def get_used_memory(self):
        return self.used

    def get_used_memory_in_percents(self):
        return self.percents_usage
