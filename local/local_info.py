import os
import time

import psutil



def get_local_utilization():
    """
    get the cpu usage and memory usage of client
    :return: cpu usage and memory usage
    """
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    return cpu_usage, memory_usage


def update_local_utilization(local_cpu_usage, local_memory_usage):

    while os.getppid():

        cpu_usage, memory_usage = get_local_utilization()
        local_cpu_usage.value = cpu_usage
        local_memory_usage.value = memory_usage
        time.sleep(10)
        print("local_cpu_usage:", local_cpu_usage)
        print("local_memory_usage", local_memory_usage)

