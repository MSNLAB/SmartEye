import psutil


def get_local_utilization():
    """
    get the cpu usage and memory usage of client
    :return: cpu usage and memory usage
    """
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    return cpu_usage, memory_usage



