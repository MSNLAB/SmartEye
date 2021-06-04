import multiprocessing

from tools.read_config import read_config


def init():

    global grpc_servers
    global cpu_usage
    global memory_usage

    grpc_servers = read_config("grpc-url")
    cpu_usage = []
    memory_usage = []

    global distribution_function
    distribution_function = {
        'random': 'random_policy',
        'tasks_queue': 'shortest_queue',
        'cpu_usage': 'lowest_cpu_utilization'
    }

    global tasks_number
    tasks_number = {}
    for grpc_server in grpc_servers:
        tasks_number[grpc_server] = 0


