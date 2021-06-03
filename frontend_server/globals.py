from tools.read_config import read_config


def init():
    global grpc_servers
    grpc_servers = read_config("grpc-url")
    global distribution_function
    distribution_function = {
        'random': 'random_policy',
        'tasks_queue': 'shortest_queue',
        'cpu_usage': 'lowest_cpu_utilization'
    }
    global cpu_usage
    cpu_usage = []
    global memory_usage
    memory_usage = []
    global tasks_number
    tasks_number = {}
    for grpc_server in grpc_servers:
        tasks_number[grpc_server] = 0
