import random
import frontend_globals


def random_policy():
    """Choose a random server from all of the servers and return.

    :return: server url
    """
    rand = random.randint(0, len(frontend_globals.grpc_servers) - 1)
    key = frontend_globals.grpc_servers[rand]
    return key


def shortest_queue():
    """Choose a grpc server whose tasks queue is the shortest.

    :return: server url
    """
    tasks_number_list = frontend_globals.tasks_number.values()
    selected_server = tasks_number_list.index(min(tasks_number_list))
    key = frontend_globals.grpc_servers[selected_server]
    return key


def lowest_cpu_utilization():
    """Get the server url whose cpu utilization is the lowest one.

    :return: server url
    """
    selected_server = frontend_globals.cpu_usage.index(min(frontend_globals.cpu_usage))
    key = frontend_globals.grpc_servers[selected_server]
    return key




