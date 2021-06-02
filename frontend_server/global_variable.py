from tools.read_config import read_config


def init():
    global grpc_servers
    grpc_servers = read_config("grpc-url")
    global tasks_number_dict
    tasks_number_dict = {}
    for grpc_server in grpc_servers:
        tasks_number_dict[grpc_server] = 0
