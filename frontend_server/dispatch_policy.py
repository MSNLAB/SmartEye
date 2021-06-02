import random
from tools.read_config import read_config


def random_policy():
    grpc_servers = read_config("grpc-url")
    rand = random.randint(0, len(grpc_servers)-1)
    return grpc_servers[rand]


def shortest_queue():
    pass


def lowest_cpu_utilization():
    cpu_usage_list = []
    for grpc_server in grpc_servers:
        load_specified_model(grpc_server, "densenet121")
        # cpu_usage = get_cpu_usage(grpc_server)
        models = get_loaded_models(grpc_server)
        print(models)
        cpu_usage_list.append(cpu_usage)
    print(cpu_usage_list)
    selected_server = cpu_usage_list.index(min(cpu_usage_list))
    return grpc_servers[selected_server]

