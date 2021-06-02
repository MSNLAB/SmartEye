import random

from frontend_server.grpc_interface import get_server_utilization
from tools.read_config import read_config
import global_variable


def random_policy():
    """
    choose a random server from all of the servers and return.
    :return: server url
    """
    rand = random.randint(0, len(global_variable.grpc_servers)-1)
    key = global_variable.grpc_servers[rand]
    global_variable.tasks_number_dict[key] += 1
    print(global_variable.tasks_number_dict)
    return key


def shortest_queue():
    """
    choose
    """
    tasks_number_list = global_variable.tasks_number_dict.values()
    selected_server = tasks_number_list.index(min(tasks_number_list))
    key = global_variable.grpc_servers[selected_server]
    global_variable.tasks_number_dict[key] += 1
    return key


def lowest_cpu_utilization():
    """
    get the server url whose cpu utilization is the lowest one.
    :return: server url
    """
    cpu_usage_list = []
    memory_usage_list = []
    for grpc_server in global_variable.grpc_servers:
        cpu_usage, memory_usage = get_server_utilization(grpc_server)
        cpu_usage_list.append(cpu_usage)
        memory_usage_list.append(memory_usage)
    selected_server = cpu_usage_list.index(min(cpu_usage_list))
    key = global_variable.grpc_servers[selected_server]
    global_variable.tasks_number_dict[key] += 1
    return key

