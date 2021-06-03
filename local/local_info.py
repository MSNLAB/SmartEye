import psutil
import globals


def get_local_utilization():
    """
    get the cpu usage and memory usage of client
    :return: cpu usage and memory usage
    """
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    return cpu_usage, memory_usage


def processor_decision():
    """
    decide to choose local processor or remote processor
    :return: 'local' for local processor and 'remote' for remote processor
    """
    cpu_usage = globals.local_cpu_usage
    memory_usage = globals.local_memory_usage
    if cpu_usage < 0 and memory_usage < 0:
        return "local"
    else:
        return "remote"
