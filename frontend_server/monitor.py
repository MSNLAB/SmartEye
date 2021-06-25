from loguru import logger
import frontend_globals
from frontend_server.grpc_interface import get_server_utilization


def server_monitor():
    """Update the cpu usage list and memory usage list every ten seconds.

    :return: None
    """
    frontend_globals.cpu_usage = []
    frontend_globals.memory_usage = []
    for grpc_server in frontend_globals.grpc_servers:
        new_cpu_usage, new_memory_usage = get_server_utilization(grpc_server)
        frontend_globals.cpu_usage.append(new_cpu_usage)
        frontend_globals.memory_usage.append(new_memory_usage)
    logger.info("cpu_usage:" + str(frontend_globals.cpu_usage))
    logger.info("memory_usage" + str(frontend_globals.memory_usage))

