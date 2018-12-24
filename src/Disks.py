import psutil as ps
from Partition import Partition

class Disks:
    def __init__(self):
        self.partitions = self.create_partitions_info()
    
    def find_partitions(self):
        partitions = ps.disk_partitions()
        partitions = [prt for prt in partitions if not prt.mountpoint.startswith('/snap')]
        return partitions

    def disk_usage_for_partitions(self):
        partitions = self.find_partitions()
        partitions_usage = [ps.disk_usage(prt.mountpoint) for prt in partitions]
        return list(zip(partitions, partitions_usage))

    def create_partitions_info(self):
        info = self.disk_usage_for_partitions()
        return [Partition(partition, usage) for partition, usage in info]

    def get_partitions(self):
        for prt in self.partitions:
            yield prt