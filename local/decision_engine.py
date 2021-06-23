import edge_globals
from config.model_info import edge_object_detection_model
from config.model_info import cloud_object_detection_model
from model_manager.model_cache import get_fastest_model
from loguru import logger

resolution_list = [(240, 352), (360, 480), (480, 858), (720, 1280)]
qp_value = [30, 40, 50, 60, 70, 80, 90]


# the video frame will be always processed on edge
def always_local_fastest_model(task):
    task.location = edge_globals.LOCAL
    if task.serv_type == edge_globals.OBJECT_DETECTION:
        task.selected_model = get_fastest_model(edge_object_detection_model)
       # logger.debug(task.selected_model)
    return task


# the video frame will be always processed on the cloud
def always_cloud_lowest_delay(task):
    
    task.location = edge_globals.OFFLOAD
    task.new_size = resolution_list[0]
    logger.debug("task.serv_type"+str(task.serv_type))
    if task.serv_type == edge_globals.OBJECT_DETECTION:
        #task.selected_model = get_fastest_model(cloud_object_detection_model)
        task.selected_model = 'retinanet_resnet50_fpn'  
        logger.debug("decision:"+task.selected_model)
    return task


def threshold_offload_policy(task):
    pass


def delay_precision_tradeoff(task):
    pass


class DecisionEngine:

    def __init__(self, sys_info):
        self.sys_info = sys_info
        self.policy_set = {"always_local_fastest_model": always_local_fastest_model,
                           "always_cloud_lowest_delay": always_cloud_lowest_delay}
        self.last_frame = None

    def get_decision(self, policy, task):
        # make decision based on the policy
        task = self.policy_set[policy](task)
        # save the frame for differencing in the next time
        self.last_frame = task.frame
        return task


