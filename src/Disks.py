import psutil as ps
from Partition import Partition

class Disks:
    def __init__(self):
        self.partitions = self.create_partitions_info()
    
    def find_partitions(self):
        return [prt for prt in ps.disk_partitions() if not prt.mountpoint.startswith('/snap')]

    def disk_usage_for_partitions(self):
        return [(prt, ps.disk_usage(prt.mountpoint)) for prt in self.find_partitions()]

    def create_partitions_info(self):
        return [Partition(partition, usage) for partition, usage in self.disk_usage_for_partitions()]

    def get_partitions(self):
        return self.partitions