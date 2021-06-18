import os
import time
import psutil


def get_local_utilization():
    """Get the CPU usage and memory usage
    :return: cpu usage and memory usage
    """
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage


def update_local_utilization(local_cpu_usage, local_memory_usage):
    """Update local utilization including cpu usage and memory usage

    :param local_cpu_usage: local cpu usage
    :param local_memory_usage: local memory usage
    :return: None
    """
    cpu_usage, memory_usage = get_local_utilization()
    local_cpu_usage.value = cpu_usage
    local_memory_usage.value = memory_usage

