from loguru import logger
import globals
from frontend_server.grpc_interface import get_server_utilization


def server_monitor():
    """Update the cpu usage list and memory usage list every ten seconds.

    :return: None
    """
    globals.cpu_usage = []
    globals.memory_usage = []
    for grpc_server in globals.grpc_servers:
        new_cpu_usage, new_memory_usage = get_server_utilization(grpc_server)
        globals.cpu_usage.append(new_cpu_usage)
        globals.memory_usage.append(new_memory_usage)
    # print("cpu_usage:", globals.cpu_usage)
    # print("memory_usage", globals.memory_usage)
    logger.info("cpu_usage:" + str(globals.cpu_usage))
    logger.info("memory_usage" + str(globals.memory_usage))

