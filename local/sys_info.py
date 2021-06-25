import time
import psutil
import collections
from loguru import logger


Data = collections.namedtuple('Data', ['time', 'value'])


def get_local_utilization():
    """Get the CPU usage and memory usage"""
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage


class SysInfo:
    """Storing the system information of local and server"""
    def __init__(self):
        
        self.cpu_usage = []
        self.memory_usage = []
        self.local_delay = []
        self.offload_delay = []
        self.bandwidth = []
        self.local_pending_task = 0

    def update_local_utilization(self):
        """Update local utilization including cpu usage and memory usage"""
        t = time.time()
        
        cpu_usage, memory_usage = get_local_utilization()
        self.cpu_usage.append(Data(t, cpu_usage))
        self.memory_usage.append(Data(t, memory_usage))

    def append_local_delay(self, cur_time, delay):
    
        data = Data(cur_time, delay)
        self.local_delay.append(data)

    def append_offload_delay(self, cur_time, delay):

        data = Data(cur_time, delay)
        self.offload_delay.append(data)

    def append_bandwidth(self, cur_time, delay):
        data = Data(cur_time, delay)
        self.bandwidth.append(data)





