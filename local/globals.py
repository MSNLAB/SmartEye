import multiprocessing


def init():

    global local_cpu_usage
    local_cpu_usage = multiprocessing.Value("d", 0)

    global local_memory_usage
    local_memory_usage = multiprocessing.Value("d", 0)


