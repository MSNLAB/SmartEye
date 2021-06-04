import os
import random
import time
from frontend_server.grpc_interface import get_server_utilization
import globals


def random_policy():
    """
    choose a random server from all of the servers and return.
    :return: server url
    """
    rand = random.randint(0, len(globals.grpc_servers)-1)
    key = globals.grpc_servers[rand]
    return key


def shortest_queue():
    """
    choose a grpc server whose tasks queue is the shortest.
    :return: server url
    """
    tasks_number_list = globals.tasks_number.values()
    selected_server = tasks_number_list.index(min(tasks_number_list))
    key = globals.grpc_servers[selected_server]
    return key


def lowest_cpu_utilization():
    """
    get the server url whose cpu utilization is the lowest one.
    :return: server url
    """
    selected_server = globals.cpu_usage.index(min(globals.cpu_usage))
    key = globals.grpc_servers[selected_server]
    return key


def update_cpu_and_memory_usage(grpc_servers_proxy, cpu_usage_proxy, memory_usage_proxy):
    """
    update the cpu usage list and memory usage list every ten seconds.
    :return: None
    """
    while os.getppid():

        cpu_usage_proxy = []
        memory_usage_proxy = []
        for grpc_server in grpc_servers_proxy:
            new_cpu_usage, new_memory_usage = get_server_utilization(grpc_server)
            cpu_usage_proxy += [new_cpu_usage]
            memory_usage_proxy += [new_memory_usage]
        time.sleep(10)

        print("cpu_usage:", cpu_usage_proxy)
        print("memory_usage", memory_usage_proxy)

